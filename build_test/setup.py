from cx_Freeze import setup, Executable

setup(name = "Password generator" ,
     version = "1.0.0" ,
     description = "Test" ,
     executables = [Executable("password_generator.py", base = "Win32GUI")])