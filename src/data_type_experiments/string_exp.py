hello_world: str = "Hello World!"


def print_hello():
    print(hello_world)


def hello_to(name: str):
    print(f"Hello, {name}")


print_hello()
hello_to("Nazar")

name = "John popo"
print(name.upper())


site = "https://www.google.com"
print(site.removeprefix("https://"))
print(site.removesuffix(".com"))
print(site.endswith(".com"))
print(site.startswith("https://"))


def check_protocol(actual_url: str):
    if actual_url.startswith("https://"):
        print(f"{actual_url} is correct")
    else:
        print(f"{actual_url} is insecure")


check_protocol("https://www.google.com")
check_protocol("http://www.google.com")
