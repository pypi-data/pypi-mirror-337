try:
    from . import modul2  # Nur von Außerhalb des Pakets
except ImportError:
    import modul2  # Nur innerhalb des Pakets
#>>>
# def funktion2():
#     print("Grüße aus 2!")
    
# funktion2()

print(f"ModulA: {__name__=}")
def funktion1():
    print("Grüße aus 1!")
    