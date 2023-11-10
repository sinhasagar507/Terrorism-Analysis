import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import plotly.express as px
import streamlit as st

warnings.filterwarnings("ignore")

st.set_page_config(layout="wide")
from streamlit_option_menu import option_menu
from tqdm import tqdm


def main():
    terr_data = pd.read_csv("data/combined_data.csv")
    with st.sidebar:
        choose = option_menu("Welcome", ["Description", "Exploratory Analysis", "Code"],
                             icons=['table', 'bar-chart', 'cpu'],
                             menu_icon='building', default_index=0,
                             styles={
                                 "container": {"padding": "5!important", "background-color": "#1a1a1a"},
                                 "icon": {"color": "White", "font-size": "25px"},
                                 "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                              "--hover-color": "#4d4d4d"},
                                 "nav-link-selected": {"background-color": "#4d4d4d"},
                             })

    if choose == "Description":
        st.markdown("<h1 style='text-align: left;'>Terrorism in South Asia</h1>", unsafe_allow_html=True)
        st.markdown('''
        <p style='text-align: justify;'>The analysis is based upon the <a href="https://www.start.umd.edu/gtd/">Global Terrorism Data(GTD)</a>, 
        which is an event-level database consisting of more than 200,000 records of terrorist attacks which have plagued the world since 1970. 
        In this mini-project, I have specifically visualized data for the South Asian region, which consists of Pakistan, India, Afghanistan, 
        Sri Lanka, Bangladesh, Nepal, Maldives, Mauritius and Bhutan.</p>
        ''', unsafe_allow_html=True)

        with st.expander("Expanded view of the overall dataset👉"):
            st.dataframe(terr_data.head())
            st.table(terr_data.describe())

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(''' 
                <h3>Perpetrator(s)</h3>
            <p>Captures information concerning terrorists</p>
            <p>A brief description of parameters associated with this information is as follows:</p>
            <ul> 
                   <li>gname - Perpetrator group name</li>
                   <li>nperpcap - This field records the number of perpetrators taken into custody</li>
                   <li>nperps - This field records the total number of terrorists participating in the incident</li>
            </ul> 
            <br>
            <h3>Target(s)/Victim(s)</h3>
            <p>Captures information concerning terrorist attack victims</p>
            <p>A brief description of relevant target information is as follows:</p>
            <ul> 
                   <li>targtype - Perpetrator group name</li>
                   <li>targsubtype - This field records the number of perpetrators taken into custody</li>
                   <li>corp - Name of corporate organization or government entity that was attacked</li>
            </ul> 
            <br> 
            <h3>Incident Criteria</h3>
            <p>Information with respect to conducted terrorist activity</p>
            <p>A brief description of relevant incident information is as follows:</p>
            <ul> 
                   <li>crit1 - Criteria to determine if an attack attack was aimed at achieving a particular political, economic, religious or social goal</li>
                   <li>crit2 - Criteria to determine if an attack was aimed to coerce, intimidate or publicize to larger audiences</li>
                   <li>crit3 - Criteria to determine if an attack was outside the precincts of international humanitarian law</li> 
                   <li>doubtterr - A binary label which encodes the "uncertainty" regarding the qualification of a terrorist attack</li>
                   <li>multiple - A binary label which encodes if the specific attack is part of a multiple co-ordinated attack</li>
                   <li>related - Lists GTD IDs of all other associated terrorist attacks, if it qualifies the "multiple" criterion</li>
            </ul> 
            <br>
            <h3>Location Information</h3>
            <p>Information concerning the location of terrorist attacks</p>
            <p>A brief description of relevant location information is as follows:</p>
            <ul> 
                   <li>country - Country where the terrorist attack took place </li>
                   <li>province - State/province of attack </li>
                   <li>city - City of attack </li>
                   <li>vicinity - Indicates if the attack took place in the vicinity of cities</li>
                   <li>latitude - Latitude of location where the attack took place</li>
                   <li>longitude - Longitude of location where the attack took place</li>
                   <li>geometry - Geometrical point co-ordinate where the attack occured</li>
            </ul>
            <br>
            <h3>Event Date</h3>
            <p>Information concerning when such attacks were conducted</p>
            <p>A brief description of parameters associated with this information is as follows:</p>
            <ul> 
                   <li>eventid - EventID </li>
                   <li>iyear - Year in which the attack took place</li>
                   <li>imonth - Month of attack</li>
                   <li>iday - Day of attack</li>
                   <li>imonth - Indicates if the attack spanned across multiple days</li>
            </ul> 
            <br>
            <h3>Weapons</h3>
                <p>Data on up to four types and sub-types of the weapons used in the attack are recorded for each case, in addition 
                to any information on specific weapon details reported.</p>
                <p>A brief description of parameters associated with this information is as follows:</p>
                <ul> 
                       <li>weaptype - Perpetrator group name</li>
                       <li>weapsubtype - This field records the number of perpetrators taken into custody</li>
            </ul> 
            <br>
            <h3>Casualties</h3>
            <p>Information concerning loss of life and property as a result of terrorist attacks</p>
            <p>A brief description of parameters associated with this information is as follows:</p>
            <ul> 
                   <li>nkill - Count of victim fatalities</li>
                   <li>nkillter - Count of terrorist fatalities</li>
                   <li>nwound - Count of victims wounded in the attack</li>
                   <li>nwoundte - Count of terrorists wounded in the attack</li>
                   <li>property- If property damage has occured from the incident</li>
                   <li>ishostkid- Records whether or not the victims were taken hostage</li>        
            </ul> 
        
        ''', unsafe_allow_html=True)

    elif choose == "Exploratory Analysis":


        def select_widget(label, valuetup, key):
            return st.selectbox(
                label,
                options=valuetup,
                key=key
            )


        def set_labels(ax, xlabel, ylabel, x_fontsize, y_fontsize):
            ax.set_xlabel(xlabel, fontsize=x_fontsize, labelpad=15)
            ax.set_ylabel(ylabel, fontsize=y_fontsize, labelpad=14)


        def countplot(df, parameter, criteria):
            fig = plt.figure(figsize=(7, 5))

            if parameter == "targettype" and criteria is None:
                ax = sns.countplot(data=df, y=parameter)
                set_labels(ax, "Count", "Target Type", 13, 13)
                return fig

            elif parameter == "weaptype" and criteria is None:
                ax = sns.countplot(y=parameter, data=df, palette=["tomato"])
                set_labels(ax, "Count", "Attack Weapon", x_fontsize=10, y_fontsize=10)
                return fig

            elif parameter == "country" and criteria is None:
                ax = sns.countplot(y=parameter, data=df, palette="pastel")
                set_labels(ax, "Count", "Country Of Attack", x_fontsize=10, y_fontsize=10)
                return fig

            elif parameter == "alternative_attack_type" and criteria is not None:
                title_text = "Political, Economic or Religious Goal"
                if criteria == "crit2":
                    title_text = "Coercion and Intimidation"
                elif criteria == "crit3":
                    title_text = "Illegitimate Warfare"
                ax = sns.countplot(data=df, y=parameter, hue=criteria,
                                   palette=["tomato", "limegreen"])
                set_labels(ax, "Count", "Alternative Attack Type", x_fontsize=10, y_fontsize=10)
                ax.legend(title=title_text, loc="lower right", labels=["No", "Yes"])
                return fig


        def densityplot(geo_df, country, year, color_hue):
            geo_df = geo_df[(geo_df["country"] == country) & (geo_df["iyear"] == year)]
            fig = px.scatter_mapbox(geo_df, lat="latitude", lon="longitude", size=color_hue,
                                    hover_name="tooltip_text", hover_data=["latitude", "longitude"],
                                    mapbox_style="open-street-map", width=1500)
            return fig


        def geoplot(geo_df, country, year, color_hue):
            geo_df = geo_df[(geo_df["country"] == country) & (geo_df["iyear"] == year)]
            fig = px.scatter_geo(geo_df, lat=geo_df["geometry"].x, lon=geo_df["geometry"].y, hover_name="tooltip_text",
                                 color=color_hue, size="casualties", scope="asia", projection="natural earth",
                                 width=1500)

            # Reset the legend title
            fig.update_layout(legend=dict(title="Attack Type"))
            return fig

        st.markdown("<h1 style='text-align: center;'>Data Analysis</h1>", unsafe_allow_html=True)
        st.markdown("")
        st.markdown("<h3 style='text-align: center;'>Terrorist Group Involvement</h3>", unsafe_allow_html=True)
        st.markdown("")
        col1, col2 = st.columns([1.5, 2], gap="large")

        with col1:
            st.markdown('''
            <p style='text-align: justify;'> The chart portrays the proportional representation of different terrorist organizations involved
            in the attack. "Unknown" names refers to unrecognized or unidentified terror outfits. It is plausible that most of the terrorist 
            attacks were not reported or documented by the governments and security agencies.</p>
                ''', unsafe_allow_html=True)

        with col2:
            def my_autopct(pct):
                return ("%.2f%%" % pct) if pct > 10 else ""

            top_perp_info = terr_data["gname"].value_counts().sort_values(ascending=False).head(10).to_dict()
            df_perp_info = pd.DataFrame(data=top_perp_info.values(), index=top_perp_info.keys(),
                                        columns=["Attack_count"])
            labels = df_perp_info.index
            values = df_perp_info["Attack_count"]
            fig, ax = plt.subplots(figsize=(18, 14), subplot_kw=dict(aspect="equal"))
            myexplode = [0.05, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ax.pie(values, shadow=True, startangle=90, autopct=my_autopct, pctdistance=0.6, explode=myexplode,
                   textprops={"fontsize": 20})
            ax.axis("equal")
            ax.legend(labels, loc='upper right', bbox_to_anchor=(1.3, 0.9), fontsize=15)
            st.pyplot(fig)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>Entity Frequency Analysis</h3>", unsafe_allow_html=True)
            st.markdown("")

            df_terr = terr_data[terr_data["doubtterr"] == 0]
            df_notterr = terr_data[terr_data["doubtterr"] != 0]

        col1f, col2f = st.columns([1.5, 2], gap="large")

        with col1f:
            selected_option = select_widget(
                "Which attribute do you want to analyze?",
                ("Target Type", "Alternative Attack Type", "Weapon", "Country"),
                "Attribute"
            )

            if selected_option == "Target Type":
                col1f.markdown(
                    "<p style='text-align: justify;'> Civilians were the major targets in most of the attacks, followed by police and military. </p>",
                    unsafe_allow_html=True)

            elif selected_option == "Alternative Attack Type":
                col1f.markdown(
                    "<p style='text-align: justify;'>Alternative attacks refer to unconfirmed violent acts which have not been confirmed as terrorist activities by governments and security agencies</p>",
                    unsafe_allow_html=True)
                selected_criteria = select_widget("Inclusion criteria for doubtful terrorist attacks?",
                                                  ("Personal Motive", "Coercion and Intimidation",
                                                   "Illegitimate Warfare"))

                if selected_criteria == "Personal Motive":
                    col1f.markdown('''
                        <p style='text-align: justify;'>The violent act must be aimed at attaining a political, economic or social goal. 
                        This criterion is not satisfied in those cases where the perpetrator(s) acted out of a pure profit motive or from 
                        an idiosyncratic personal motive unconnected with broader societal change</p>
                        ''', unsafe_allow_html=True)

                elif selected_criteria == "Coercion and Intimidation":
                    col1f.markdown('''
                        <p style='text-align: justify;'col1fo satisfy this criterion there must be evidence of an intention to coerce, intimidate,
                        or convey some other some other message to a larger audience (or audiences) than the immediate victims. Such evidence 
                        can include (but is not limited to) the following: pre- or post-attack statements by the perpetrator(s), past behavior by the perpetrators, 
                        or the particular nature of the target/victim, weapon, or attack type
                        ''', unsafe_allow_html=True)

                else:
                    col1f.markdown('''
                       <p style='text-align: justify;'>The action is outside the context of legitimate warfare activities, insofar as it targets          
                       non-combatants, i.e., the act must be outside the parameters permitted by international humanitarian law as reflected in the 
                       Additional Protocol to the Geneva Conventions of 12 August 1949 and elsewhere</p>
                       ''', unsafe_allow_html=True)

            elif selected_option == "Weapon":
                col1f.markdown(
                    "<p>Explosives and firearms were used a lot more than any other weapon in carrying out terrorist activities</p>",
                    unsafe_allow_html=True)

            else:
                col1f.markdown("<p>Afghanistan has witnessed significantly more attacks than any other country</p>",
                               unsafe_allow_html=True)

        with col2f:
            if selected_option == "Target Type":
                col2f.pyplot(countplot(terr_data, "targettype", None))

            elif selected_option == "Alternative Attack Type":
                if selected_criteria == "Personal Motive":
                    col2f.pyplot(countplot(df_notterr, "alternative_attack_type", "crit1"))

                elif selected_criteria == "Coercion and Intimidation":
                    col2f.pyplot(countplot(df_notterr, "alternative_attack_type", "crit2"))

                else:
                    col2f.pyplot(countplot(df_notterr, "alternative_attack_type", "crit3"))

            elif selected_option == "Weapon":
                col2f.pyplot(countplot(df_notterr, "weaptype", None))

            else:
                col2f.pyplot(countplot(df_notterr, "country", None))

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Terrorist Activities vs. other Militant Attacks</h3>",
                    unsafe_allow_html=True)
        st.markdown("")
        col1c, col2c = st.columns([1, 1], gap="large")

        with col1c:
            g = sns.FacetGrid(df_terr, col="crit3", row="crit2")
            g.map(sns.countplot, "crit1")
            st.pyplot(g)
            st.markdown('''
            <p style='text-align: justify;'>It is confirmed that not only all terrorists have a personal agenda, but they also have a proclivity 
            for intimidating people through horrendous and inhuman methods</p>
            ''', unsafe_allow_html=True)

        with col2c:
            g1 = sns.FacetGrid(df_notterr, col="crit3", row="crit2")
            g1.map(sns.countplot, "crit1")
            st.pyplot(g1)
            st.markdown('''
            <p style='text-align: justify;'>Other unreported militant activities flout humanitarian laws, but their agenda or motivation cannot
            be perfectly established</p>
            ''', unsafe_allow_html=True)

        st.markdown("")

        st.markdown("<h4 style='text-align: center;'></h4>", unsafe_allow_html=True)
        st.write("")
        year_kills = pd.DataFrame(terr_data.groupby(["iyear", "country"])["success"].count().reset_index())
        year_kills = year_kills.loc[:, ~year_kills.columns.duplicated()]
        year_kills["kills"] = terr_data.groupby(["iyear", "country"])["nkill"].sum().values
        year_kills["wounded"] = terr_data.groupby(["iyear", "country"])["nwound"].sum().values
        year_kills["kill_ratio"] = np.round(((year_kills["kills"]) / (year_kills["kills"] + year_kills["wounded"] + 1)),
                                            3)
        fig_scatter = px.scatter(year_kills, x="iyear", y="kill_ratio", color="country", size="success")
        fig_scatter.update_layout(title="Fatality-Casualty Ratio", title_x=1)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown('''
        <p style='text-align: justify;'><b>Click on different country names in the legend to hide their representation in the plot.</b>
        We can infer that significantly larger number of terrorist attacks have been perpetrated during the time period from 2007-2017, 
        particularly in Afghanistan, Pakistan and India. Moreover, the period witnessed higher number of fatalities during this period.</p>
        ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align: center;'>Civilian Deaths in Terrorist Attacks</h3>",
                    unsafe_allow_html=True)

        st.markdown("")
        rel_attacks_ls = []
        geo_data = gpd.GeoDataFrame(terr_data, geometry=gpd.points_from_xy(terr_data["latitude"],
                                                                           terr_data["longitude"]))
        geo_data = geo_data.loc[:, ~geo_data.columns.duplicated()]
        geo_data = geo_data[
            ["latitude", "longitude", "geometry", "city", "country", "casualties", "attacktype", "eventid", "iyear",
             "related"]]
        geo_data["tooltip_text"] = geo_data["city"] + ", " + geo_data["country"]
        geo_data_rel = geo_data[geo_data["related"] != "Unknown"]
        geo_data_rel = geo_data_rel.reset_index()
        geo_data_rel = geo_data_rel.drop("index", axis=1)
        for idx in tqdm(geo_data_rel.index):
            rel_ls = list(geo_data_rel.loc[idx, "related"].split(","))
            rel_ls.append(str(geo_data_rel.loc[idx, "eventid"]))
            rel_ls.sort()
            if rel_ls not in rel_attacks_ls:
                rel_attacks_ls.append(rel_ls)

        def append_event_id(row):
            rel_ls = row["related"].split(",")
            rel_ls.append(str(row["eventid"]))
            rel_ls.sort()
            return rel_ls

        geo_data_rel["events"] = geo_data_rel.apply(lambda rowval: append_event_id(rowval), axis=1)
        geo_data_rel["event_key"] = geo_data_rel["events"].apply(lambda val: rel_attacks_ls.index(val))
        geo_data_rel["event_key"] = geo_data_rel["event_key"].astype("int64")

        col1d, col2d = st.columns([1, 1], gap="large")

        with col1d:
            country_select = select_widget(
                "Select Country",
                ("India", "Afghanistan", "Pakistan", "Bangladesh", "Sri Lanka", "Bhutan", "Maldives", "Nepal"),
                "Country1"
            )

        with col2d:
            year_select = select_widget(
                "Select Year",
                tuple(geo_data_rel["iyear"].unique()),
                "Year1"
            )

        st.plotly_chart(densityplot(geo_data_rel, country_select, year_select, "casualties"), use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Weapon Category across Countries</h3>",
                    unsafe_allow_html=True)
        st.markdown("")

        col1e, col2e = st.columns([1, 1], gap="large")

        with col1e:
            country_weapon_select = select_widget(
                "Select Country",
                ("India", "Afghanistan", "Pakistan", "Bangladesh", "Sri Lanka", "Bhutan", "Maldives", "Nepal"),
                "Country2"
            )

        with col2e:
            country_year_select = select_widget(
                "Select Year",
                tuple(geo_data_rel["iyear"].unique()),
                "Year2"
            )

            st.plotly_chart(geoplot(geo_data, country_weapon_select, country_year_select, "attacktype"),
                            use_container_width=True)


if __name__ == "__main__":
    main()
