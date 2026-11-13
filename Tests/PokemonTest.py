import pokemon

names = [None, "Bulbasaur", "Ivysaur", "Venusaur"]
hg, ss = [None,  "Pallet Town", "Evolve Bulbasaur", "Evolve Ivysaur"], [None, "Pallet Town", "Evolve Bulbasaur", "Evolve Ivysaur"]
pokemon = [None]


[pokemon.append(Pokemon.Pokemon(i, names[i], None, None, None, hg[i], ss[i], False, None, None, None)) for i in range(1, 4)]


# assert pokemon[1].dex == 1, f"Expecting: 1.  Actual {pokemon[1].dex}"
# assert pokemon[1].name == "Bulbasaur", f"Expecting: Bulbasaur.  Actual {pokemon[1].dex}"
# assert pokemon[3].dex == 3, f"Expecting: 3.  Actual {pokemon[3].dex}"
# assert pokemon[3].name == "Venusaur", f"Expecting: Venusaur.  Actual {pokemon[3].name}"
# print(pokemon[1])
#
# print("Passed tests!")