from typing import NamedTuple, Literal
from subprocess import Popen, PIPE, STDOUT

from exceptions import CantGetCoordinates


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_coordinates() -> Coordinates:
    """Returns current coordinates using Windows System.Device"""
    coordinates = _get_windows_coordinates()
    return coordinates


def _get_windows_coordinates() -> Coordinates:
    powershell_output = _get_powershell_output()
    coordinates = _parse_coordinates(powershell_output)
    return coordinates


def _get_powershell_output() -> bytes:
    pshellcomm = ['powershell', 'Add-Type -AssemblyName System.Device;'
                                '$loc = New-Object System.Device.Location.GeoCoordinateWatcher;'
                                '$loc.Start();'
                                'start-sleep -milliseconds 100;'
                                '$loc.position.location.latitude;'
                                '$loc.position.location.longitude;']

    process = Popen(pshellcomm, stdout=PIPE, stderr=STDOUT)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if err or exit_code:
        raise CantGetCoordinates
    return output


def _parse_coordinates(ps_output: bytes) -> Coordinates:
    try:
        output = ps_output.decode('CP866').strip().lower().split('\r\n')
    except UnicodeDecodeError:
        raise CantGetCoordinates
    return Coordinates(
        latitude=_parse_coord(output, 'latitude'),
        longitude=_parse_coord(output, 'longitude')
    )


def _parse_coord(output: list[str], coord_type: Literal['latitude', 'longitude']) -> float:
    try:
        match coord_type:
            case 'latitude':
                return _parse_float_coord(output[0].replace(',', '.'))
            case 'longitude':
                return _parse_float_coord(output[1].replace(',', '.'))
    except IndexError:
        raise CantGetCoordinates


def _parse_float_coord(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise CantGetCoordinates


if __name__ == '__main__':
    print(get_coordinates())
