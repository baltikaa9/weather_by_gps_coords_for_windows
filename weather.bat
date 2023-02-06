@echo off
::set cur_dir=%cd%
F:
call F:\Projects\PycharmProjects\weather\venv\Scripts\activate
cd F:\Projects\PycharmProjects\weather

python weather.py

C:
deactivate
::cd %cur_dir%