string = "static\Rene_Ramirez_application.html"
firstName = string[string.index("\\")+1:string.index("_")]
lastName = string[string.index("_") + 1:string.index("application")-1]

print(firstName)
print(lastName)