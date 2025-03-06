import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import plotly.express as px

def main():
    # Load the dataset
    df = pd.read_excel('AFFICHAGE.xlsx', sheet_name='Data')

    # Set the title of the Streamlit app
    st.title('Dashboard OOH 2024')

    # Display the dataframe
    st.write('Apercu des données', df.head())

    # Titre de l'application
    st.header('Quelques indicateurs')
    
    hex = '#B10100'
    
    # Calculer les indicateurs
    num_rows = df.shape[0]
    revenu = df["Prix"].sum()
    annonceur = df["Annonceurs"].nunique()
    secteurs = df["Secteurs d'activités"].nunique()
    villes = df["Villes"].nunique()

    # Utilisation de conteneurs pour styliser les indicateurs
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown("""
        <div class="indicator-container">
            <div class="indicator-icon">📪</div>
            <div class="indicator-title">Nombre de campagnes</div>
            <div class="indicator-value">{}</div>
        </div>
        """.format(num_rows), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="indicator-container">
            <div class="indicator-icon">📢</div>
            <div class="indicator-title">Nombre d'Annonceurs</div>
            <div class="indicator-value">{}</div>
        </div>
        """.format(annonceur), unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="indicator-container">
            <div class="indicator-icon">💰</div>
            <div class="indicator-title">Revenu Total</div>
            <div class="indicator-value">{}</div>
        </div>
        """.format(revenu), unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="indicator-container">
            <div class="indicator-icon">📊</div>
            <div class="indicator-title">Secteur d'activités</div>
            <div class="indicator-value">{}</div>
        </div>
        """.format(secteurs), unsafe_allow_html=True)
        
    with col5:
        st.markdown("""
        <div class="indicator-container">
            <div class="indicator-icon">🏙️</div>
            <div class="indicator-title">Nombre de villes couvertes</div>
            <div class="indicator-value">{}</div>
        </div>
        """.format(villes), unsafe_allow_html=True)


    st.header('Visualisation des données')
    
   

    st.subheader('Distribution geographique des campagnes 🌍')
    
    st.write('Villes par nombre de campagnes')
    top_10_villes = df['Villes'].value_counts().head(10).sort_values(ascending=True)
    fig = px.bar(top_10_villes, x=top_10_villes.values, y=top_10_villes.index, orientation='h', 
                 labels={'x': 'Nombre de campagnes', 'y': 'Villes'}, title='Top 10 des villes par nombre de campagnes',
                 color_discrete_sequence=[hex])
    st.plotly_chart(fig)

    st.write('Régions par nombre de campagnes')
    top_10_regions = df['Régions'].value_counts().head(10).sort_values(ascending=True)
    fig_regions = px.bar(top_10_regions, x=top_10_regions.values, y=top_10_regions.index, orientation='h', 
                         labels={'x': 'Nombre de campagnes', 'y': 'Régions'}, title='Top des régions par nombre de campagnes',
                         color_discrete_sequence=[hex])
    st.plotly_chart(fig_regions)
    
    st.subheader('Analyse Région-Ville-Quartier 🏙️')

    # Sélectionner une région
    region_selection = st.selectbox('Sélectionnez une région', df['Régions'].unique())

    # Filtrer les villes associées à la région sélectionnée
    villes_associees = df[df['Régions'] == region_selection]['Villes'].unique()
    ville_selection = st.selectbox('Sélectionnez une ville', villes_associees)

    # Filtrer les quartiers associés à la ville sélectionnée
    quartiers_associes = df[(df['Régions'] == region_selection) & (df['Villes'] == ville_selection)]['Quartier']

    # Trouver les 5 quartiers les plus fréquents
    top_5_quartiers = quartiers_associes.value_counts().head(5)

    # Afficher les résultats
    st.write(f'Top 5 des quartiers les plus fréquents à {ville_selection}')
    fig_quartiers = px.bar(top_5_quartiers, x=top_5_quartiers.values, y=top_5_quartiers.index, orientation='h',
                           labels={'x': 'Nombre de campagnes', 'y': 'Quartier'}, title=f'Top 5 des quartiers à {ville_selection}',
                           color_discrete_sequence=[hex])
    st.plotly_chart(fig_quartiers)
    
    st.subheader('Répartition des campagnes par secteur d\'activités  et Annonceurs 📊')
    
    st.write('Secteur d\'activités par nombre de campagnes')
    top_10_secteurs = df["Secteurs d'activités"].value_counts().head(10).sort_values(ascending=True)
    fig_secteurs = px.bar(top_10_secteurs, x=top_10_secteurs.values, y=top_10_secteurs.index, orientation='h', 
                          labels={'x': 'Nombre de campagnes', 'y': 'Secteurs d\'activités'}, title='Top 10 des secteurs d\'activités par nombre de campagnes',
                          color_discrete_sequence=[hex])
    st.plotly_chart(fig_secteurs)
    
    st.write('Secteurs d\'activités par somme des prix')
    secteurs_prix = df.groupby("Secteurs d'activités")['Prix'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_secteurs_prix = px.bar(secteurs_prix, x="Secteurs d'activités", y='Prix', 
                               labels={'Prix': 'Somme des prix', "Secteurs d'activités": 'Secteurs d\'activités'}, 
                               title='Top 10 des secteurs d\'activités par somme des prix',
                               color_discrete_sequence=[hex])
    st.plotly_chart(fig_secteurs_prix)
    
    st.subheader('Investissement par annonceurs 💼')
    
    # Calculer l'investissement total par annonceur
    investissement_annonceurs = df.groupby('Annonceurs')['Prix'].sum().sort_values(ascending=False).reset_index()

    # Créer le graphique d'investissement par annonceur
    st.write('Annonceurs par investissements consenties')
    fig_investissement_annonceurs = px.bar(investissement_annonceurs.head(10), x='Annonceurs', y='Prix',
                                           labels={'Prix': 'Investissement', 'Annonceurs': 'Annonceurs'}, 
                                           title='Top 10 des annonceurs par investissement',
                                           color_discrete_sequence=[hex])
    st.plotly_chart(fig_investissement_annonceurs)
    
    st.write('Annonceurs par nombre de campagnes')
    top_10_annonceurs = df['Annonceurs'].value_counts().head(10).sort_values(ascending=True)
    fig_annonceurs = px.bar(top_10_annonceurs, x=top_10_annonceurs.values, y=top_10_annonceurs.index, orientation='h', 
                            labels={'x': 'Nombre de campagnes', 'y': 'Annonceurs'}, title='Top 10 des annonceurs par nombre de campagnes',
                            color_discrete_sequence=[hex])
    st.plotly_chart(fig_annonceurs)
    
    st.subheader('Produits les plus affichés par région 🏷️')

    # Sélectionner une région
    region_selection_produits = st.selectbox('Sélectionnez une région pour voir les produits', df['Régions'].unique(), key='region_selection_produits')

    # Filtrer les produits associés à la région sélectionnée
    produits_associes = df[df['Régions'] == region_selection_produits]['Produits']

    # Trouver les 5 produits les plus fréquents
    top_5_produits = produits_associes.value_counts().head(5)

    # Afficher les résultats
    st.write(f'Top 5 des produits les plus affichés dans la région {region_selection_produits}')
    fig_produits = px.bar(top_5_produits, x=top_5_produits.values, y=top_5_produits.index, orientation='h',
                          labels={'x': 'Nombre de campagnes', 'y': 'Produits'}, title=f'Top 5 des produits dans la région {region_selection_produits}',
                          color_discrete_sequence=[hex])
    st.plotly_chart(fig_produits)
    
    st.subheader('Evolution du Revenu mensuel 📈')
    
    # Définir l'ordre des mois
    mois_ordre = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    
    # Calculer le revenu mensuel
    df['Mois'] = pd.Categorical(df['Mois'], categories=mois_ordre, ordered=True)
    revenu_mensuel = df.groupby('Mois')['Prix'].sum().reindex(mois_ordre).reset_index()

    # Créer le graphique de revenu mensuel
    fig_revenu_mensuel = px.line(revenu_mensuel, x='Mois', y='Prix', 
                                 labels={'Mois': 'Mois', 'Prix': 'Revenu'}, 
                                 title='Revenu mensuel',
                                 color_discrete_sequence=[hex])
    st.plotly_chart(fig_revenu_mensuel)
    
    

    
    st.subheader('Formats d\'affichages les plus utilisés 📊')
    
    # Calculer la répartition des formats d'affichages
    formats_affichages = df['Formats'].value_counts().reset_index()
    formats_affichages.columns = ['Formats', 'Nombre de campagnes']
    
    # Créer le graphique en camembert
    fig_formats_affichages = px.pie(formats_affichages, values='Nombre de campagnes', names='Formats', 
                                    title='Répartition des formats d\'affichages les plus utilisés',
                                    color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_formats_affichages)
    
    st.subheader('Word Cloud des Messages par Secteur d\'activités ☁️')

    # Sélectionner un secteur d'activités
    secteur_selection = st.selectbox('Sélectionnez un secteur d\'activités', df["Secteurs d'activités"].unique(), key='secteur_selection')

    # Filtrer les messages associés au secteur sélectionné
    messages_associes = df[df["Secteurs d'activités"] == secteur_selection]['Messages']

    # Générer le texte pour le word cloud
    text = ' '.join(messages_associes.dropna().astype(str))

    # Générer le word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Afficher le word cloud
    st.image(wordcloud.to_array(), use_container_width=True)
    
    st.subheader('Statistiques des prix par nombre de Faces 📊')
    
    # Calculer les statistiques des prix par nombre de Faces
    stats_faces = df.groupby('Faces')['Prix'].agg(['mean', 'min', 'max']).reset_index()
    stats_faces.columns = ['Nombre de Faces', 'Prix Moyen', 'Prix Minimum', 'Prix Maximum']
    
    # Afficher le tableau des statistiques
    st.write(stats_faces)
    
# Run the Streamlit app
if __name__ == '__main__':
    main()