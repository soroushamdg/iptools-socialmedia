import pathlib
data_path = str(pathlib.Path(pathlib.Path(__file__).parent).joinpath('data'))
chromdriver_path =  str(pathlib.Path(pathlib.Path(__file__).parent).joinpath('dependencies','chromedriver'))
print(data_path)


