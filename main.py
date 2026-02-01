
from modules.ai_assistant import AIAssistant

def main():
    print("IS-Assistant štartuje...")
    ai = AIAssistant()
    while True:
        print("\nZadajte typ otázky:")
        print("1 - Vyhľadaj modul")
        print("2 - Vyhľadaj funkcionalitu")
        print("q - Ukončiť")
        choice = input("Voľba: ").strip()
        if choice == '1':
            name = input("Zadajte názov modulu: ")
            print(ai.explain_module(name))
        elif choice == '2':
            name = input("Zadajte názov funkcionality: ")
            print(ai.explain_functionality(name))
        elif choice.lower() == 'q':
            print("Ukončujem IS-Assistant.")
            break
        else:
            print("Neznáma voľba. Skúste znova.")

if __name__ == "__main__":
    main()
