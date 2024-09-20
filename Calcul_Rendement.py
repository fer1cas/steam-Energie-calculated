import streamlit as st

# Pouvoir calorifique en kJ/kg pour chaque type de combustible
POUVOIR_CALORIFIQUE = {
    "Gaz": 35000,  # kJ/kg
    "LFO": 42000,  # kJ/kg
    "HFO": 40000   # kJ/kg
}

# Fonction pour obtenir l'enthalpie en fonction de la pression
def get_enthalpy(pressure):
    if pressure == 0:
        return 0  # kJ/kg (vapeur à 0 bar, pas applicable)
    elif pressure == 1:
        return 2676  # kJ/kg
    elif pressure == 2:
        return 2794  # kJ/kg
    elif pressure == 3:
        return 2827  # kJ/kg
    elif pressure == 4:
        return 2850  # kJ/kg
    elif pressure == 5:
        return 2765  # kJ/kg
    elif pressure == 6:
        return 2800  # kJ/kg
    elif pressure == 7:
        return 2810  # kJ/kg
    elif pressure == 8:
        return 2830  # kJ/kg
    elif pressure == 9:
        return 2850  # kJ/kg
    elif pressure == 10:
        return 2793  # kJ/kg
    elif pressure == 11:
        return 2900  # kJ/kg
    elif pressure == 12:
        return 2920  # kJ/kg
    elif pressure == 13:
        return 2950  # kJ/kg
    elif pressure == 14:
        return 2980  # kJ/kg
    elif pressure == 15:
        return 2930  # kJ/kg
    else:
        return None

# Fonction principale
def main():
    st.title("Calculateur de Rendement de Chaudière à Vapeur")

    # Entrées utilisateur
    debit_eau = st.number_input("Débit d'eau d'appoint (kg/h)", min_value=0.0)
    temp_eau = st.number_input("Température d'eau d'appoint (°C)", min_value=0.0)
    pression_vapeur = st.slider("Pression de vapeur (bar)", 0, 15, 1)
    debit_vapeur = st.number_input("Débit de vapeur produit (kg/h)", min_value=0.0)
    
    # Type de combustible
    type_combustible = st.selectbox("Type de combustible", ["Gaz", "LFO", "HFO"])
    
    # Entrée pour le débit de combustible
    if type_combustible == "Gaz":
        debit_combustible_m3 = st.number_input("Débit de gaz (m³/h)", min_value=0.0)
        # Conversion m³/h à kg/h (environ 0.717 kg/m³ pour le gaz naturel)
        debit_combustible = debit_combustible_m3 * 0.717  # kg/h
    else:
        debit_combustible_litre = st.number_input("Débit de combustible (litres/h)", min_value=0.0)
        # Conversion L/h à kg/h (environ 0.85 kg/L pour LFO et HFO)
        debit_combustible = debit_combustible_litre * 0.85  # kg/h

    # Calcul de l'enthalpie
    enthalpy = get_enthalpy(pression_vapeur)
    if enthalpy is None:
        st.error("Pression non supportée.")
        return

    # Calcul automatique du débit de combustible nécessaire
    pouvoir_calorifique = POUVOIR_CALORIFIQUE[type_combustible]
    debit_combustible_necessaire = (debit_vapeur * enthalpy) / pouvoir_calorifique

    # Calculs
    if debit_eau > 0:
        rendement_vapeur_eau = debit_vapeur / debit_eau
    else:
        rendement_vapeur_eau = 0
        st.warning("Le débit d'eau d'appoint doit être supérieur à zéro pour calculer le rendement.")

    # Calcul du rendement vapeur/combustible
    if debit_combustible > 0:
        energie_produite = debit_vapeur * enthalpy  # kJ
        energie_fourni = debit_combustible * pouvoir_calorifique  # kJ
        rendement_vapeur_combustible = energie_produite / energie_fourni
    else:
        rendement_vapeur_combustible = 0

    # Rendement total de la chaudière en pourcentage
    rendement_total = (rendement_vapeur_eau + rendement_vapeur_combustible) / 2 * 100

    # Calcul du taux de purge
    if debit_vapeur > 0:
        taux_purge = (debit_eau - debit_vapeur) / debit_vapeur  # kg/kg
    else:
        taux_purge = 0

    # Ratio entre le débit de combustible et le débit de vapeur
    if debit_vapeur > 0:
        ratio_combustible_vapeur = debit_combustible / debit_vapeur
    else:
        ratio_combustible_vapeur = 0

    # Affichage des résultats
    st.subheader("Résultats")
    st.write(f"Débit de combustible nécessaire pour {debit_vapeur} kg/h de vapeur : {debit_combustible_necessaire:.2f} kg/h")
    st.write(f"Débit de combustible fourni : {debit_combustible:.2f} kg/h")
    st.write(f"Ratio combustible/vapeur : {ratio_combustible_vapeur:.2f}")
    st.write(f"Rendement vapeur/eau : {rendement_vapeur_eau:.2%}")
    st.write(f"Rendement vapeur/combustible : {rendement_vapeur_combustible:.2%}")
    st.write(f"Rendement total de la chaudière : {rendement_total:.2f}%")
    st.write(f"Taux de purge : {taux_purge:.2%}")

if __name__ == "__main__":
    main()
