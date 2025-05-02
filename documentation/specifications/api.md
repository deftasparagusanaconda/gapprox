the api (application programming interface) is the main working interface of the project
the api is an instance of the class API

the api shall not handle files. thus the command tool shall also not handle input/output, and thus also not support the unix pipeline
files are sensitive things. they should be handled explicitly, not implicitly
