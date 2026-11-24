import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Simulador Cable Preensamblado 2x50+1x50",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Simulador de Producción: Cable Preensamblado")
st.subheader("CABLE PREENSAMBLADO ASC - AAAC 2 X 50 + 1 X 50 MM2 | Actual vs. Compactado")
st.markdown("Ingresa el metraje a fabricar y ajusta los costos de materia prima, tiempos o tarifas por proceso en vivo.")
st.divider()

# 1. PANEL LATERAL: VOLUMEN Y COSTOS BASE
st.sidebar.header("📏 1. Orden de Producción")
metros = st.sidebar.number_input(
    "Cantidad a fabricar (Metros):",
    min_value=1,
    max_value=1000000,
    value=1000,
    step=100
)
km = metros / 1000.0
st.sidebar.caption(f"Equivalente a: **{km:,.3f} km**")

st.sidebar.divider()
st.sidebar.header("💲 2. Costos de Materia Prima ($/kg)")
costo_al_1350 = st.sidebar.number_input(
    "ALAMBRE DE ALUMINIO 1350 9.50 MM H14 ($/kg):",
    min_value=0.0,
    value=4.2700,
    step=0.01,
    format="%.4f"
)
costo_al_6201 = st.sidebar.number_input(
    "ALAMBRE DE ALUMINIO 6201 3.00 MM ($/kg):",
    min_value=0.0,
    value=5.2416,
    step=0.01,
    format="%.4f"
)
costo_xlpe = st.sidebar.number_input(
    "XLPE NEG ($/kg):",
    min_value=0.0,
    value=2.2865,
    step=0.01,
    format="%.4f"
)

# 2. CONFIGURACIÓN DE RECETAS Y TIEMPOS
with st.expander("⚙️ Ver / Editar Parámetros Técnicos de Recetas y Tiempos de Máquina", expanded=False):
    col_rec, col_tiemp = st.columns([1.1, 1.3])
    
    with col_rec:
        st.markdown("**Consumos Unitarios por Conductor (kg/km)**")
        df_recetas = pd.DataFrame([
            {"Componente": "Fase ASC (x2) - Al 1350", "Actual (kg/km)": 135.97, "Compactado (kg/km)": 135.97},
            {"Componente": "Fase ASC (x2) - XLPE NEG", "Actual (kg/km)": 53.60, "Compactado (kg/km)": 41.00},
            {"Componente": "Neutro AAAC (x1) - Al 6201", "Actual (kg/km)": 134.17, "Compactado (kg/km)": 134.17},
            {"Componente": "Neutro AAAC (x1) - XLPE NEG", "Actual (kg/km)": 53.73, "Compactado (kg/km)": 53.73},
        ])
        recetas_edit = st.data_editor(df_recetas, hide_index=True, use_container_width=True)

    with col_tiemp:
        st.markdown("**Tiempos de Proceso por Etapa (Horas por km de conductor)**")
        st.caption("Cada etapa está vinculada a su centro de costo (Trefilado, Cableado, Extrusado, Trenzado).")
        df_tiempos = pd.DataFrame([
            {"Etapa / Máquina": "1. Trefilado Fases (x2)", "Proceso": "Trefilado", "Actual (hrs/km)": 0.45, "Compactado (hrs/km)": 0.45, "Multiplicador": 2},
            {"Etapa / Máquina": "2. Cableado Fases (x2)", "Proceso": "Cableado", "Actual (hrs/km)": 0.80, "Compactado (hrs/km)": 0.85, "Multiplicador": 2},
            {"Etapa / Máquina": "3. Extrusión XLPE Fases (x2)", "Proceso": "Extrusado", "Actual (hrs/km)": 1.10, "Compactado (hrs/km)": 0.95, "Multiplicador": 2},
            {"Etapa / Máquina": "4. Cableado + Extrusión Neutro (x1)", "Proceso": "Extrusado", "Actual (hrs/km)": 1.50, "Compactado (hrs/km)": 1.50, "Multiplicador": 1},
            {"Etapa / Máquina": "5. Reunido / Preensamblado Final (x1)", "Proceso": "Trenzado", "Actual (hrs/km)": 0.90, "Compactado (hrs/km)": 0.85, "Multiplicador": 1},
        ])
        tiempos_edit = st.data_editor(
            df_tiempos,
            hide_index=True,
            use_container_width=True,
            disabled=["Multiplicador"],
            column_config={
                "Proceso": st.column_config.SelectboxColumn(
                    "Centro de Costo",
                    options=["Trefilado", "Cableado", "Extrusado", "Trenzado"],
                    required=True
                )
            }
        )

# 3. ESTRUCTURA DE PESTAÑAS
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Comparativa Materia Prima", 
    "⏱️ Tiempos y Costos por Etapa", 
    "🏭 Costos por Proceso (Modificable)", 
    "📈 Gráficos Ejecutivos"
])

# PESTAÑA 3: COSTOS MODIFICABLES POR PROCESO
with tab3:
    st.markdown("### 🏭 Estructura de Costos de Conversión por Proceso ($/Hora-Máquina)")
    st.markdown("Edita los valores de **Mano de Obra Directa**, **Mano de Obra Indirecta** y **Costos Indirectos de Fabricación** para cada proceso. La columna **Total** se actualiza automáticamente.")
    
    df_procesos_base = pd.DataFrame([
        {
            "Proceso": "Trefilado",
            "Costo Mano de Obra Directa": 12.00,
            "Costo Mano de Obra Indirecta": 5.00,
            "Costos Indirectos de Fabricación": 18.00
        },
        {
            "Proceso": "Cableado",
            "Costo Mano de Obra Directa": 14.00,
            "Costo Mano de Obra Indirecta": 6.00,
            "Costos Indirectos de Fabricación": 22.00
        },
        {
            "Proceso": "Extrusado",
            "Costo Mano de Obra Directa": 16.00,
            "Costo Mano de Obra Indirecta": 7.50,
            "Costos Indirectos de Fabricación": 28.00
        },
        {
            "Proceso": "Trenzado",
            "Costo Mano de Obra Directa": 15.00,
            "Costo Mano de Obra Indirecta": 6.50,
            "Costos Indirectos de Fabricación": 24.00
        }
    ])
    
    procesos_edit = st.data_editor(
        df_procesos_base,
        use_container_width=True,
        hide_index=True,
        disabled=["Proceso"],
        column_config={
            "Proceso": st.column_config.TextColumn("Proceso / Línea"),
            "Costo Mano de Obra Directa": st.column_config.NumberColumn("Costo Mano de Obra Directa ($/hr)", min_value=0.0, format="$%.2f", required=True),
            "Costo Mano de Obra Indirecta": st.column_config.NumberColumn("Costo Mano de Obra Indirecta ($/hr)", min_value=0.0, format="$%.2f", required=True),
            "Costos Indirectos de Fabricación": st.column_config.NumberColumn("Costos Indirectos de Fabricación ($/hr)", min_value=0.0, format="$%.2f", required=True),
        }
    )
    
    # Calcular columna Total por proceso
    for col in ["Costo Mano de Obra Directa", "Costo Mano de Obra Indirecta", "Costos Indirectos de Fabricación"]:
        procesos_edit[col] = pd.to_numeric(procesos_edit[col], errors="coerce").fillna(0.0)
        
    procesos_edit["Total ($/hr)"] = (
        procesos_edit["Costo Mano de Obra Directa"] +
        procesos_edit["Costo Mano de Obra Indirecta"] +
        procesos_edit["Costos Indirectos de Fabricación"]
    )
    
    # Diccionario rápido para consultar tarifas por proceso
    tarifas_dict = procesos_edit.set_index("Proceso").to_dict(orient="index")
    
    st.markdown("#### 📊 Resumen de Tarifas Totales Calculadas por Proceso ($/hr)")
    cols_proc = st.columns(4)
    for idx, row in procesos_edit.iterrows():
        cols_proc[idx].metric(
            label=f"⚙️ {row['Proceso']}",
            value=f"${row['Total ($/hr)']:,.2f} / hr",
            delta=f"MOD: ${row['Costo Mano de Obra Directa']:.2f} | MOI: ${row['Costo Mano de Obra Indirecta']:.2f} | CIF: ${row['Costos Indirectos de Fabricación']:.2f}",
            delta_color="off"
        )

# Resumen rápido en barra lateral
st.sidebar.divider()
st.sidebar.header("🏭 3. Tarifas por Proceso ($/hr)")
for proc_nombre, datos_p in tarifas_dict.items():
    st.sidebar.text(f"• {proc_nombre}: ${datos_p['Total ($/hr)']:,.2f}/hr")
st.sidebar.caption("Edita el desglose en la pestaña **🏭 Costos por Proceso**.")

# 4. MOTOR DE CÁLCULO (ACTUAL VS COMPACTADO)
def calcular_escenario(tipo):
    col_val = f"{tipo} (kg/km)"
    
    al_1350_fase = recetas_edit.loc[0, col_val]
    xlpe_fase = recetas_edit.loc[1, col_val]
    al_6201_neutro = recetas_edit.loc[2, col_val]
    xlpe_neutro = recetas_edit.loc[3, col_val]
    
    kg_km_1350 = al_1350_fase * 2
    kg_km_6201 = al_6201_neutro * 1
    kg_km_xlpe = (xlpe_fase * 2) + (xlpe_neutro * 1)
    
    tot_kg_1350 = kg_km_1350 * km
    tot_kg_6201 = kg_km_6201 * km
    tot_kg_xlpe = kg_km_xlpe * km
    peso_total_kg = tot_kg_1350 + tot_kg_6201 + tot_kg_xlpe
    
    costo_tot_1350 = tot_kg_1350 * costo_al_1350
    costo_tot_6201 = tot_kg_6201 * costo_al_6201
    costo_tot_xlpe = tot_kg_xlpe * costo_xlpe
    costo_mp_total = costo_tot_1350 + costo_tot_6201 + costo_tot_xlpe
    
    col_t = f"{tipo} (hrs/km)"
    tiempos_detalle = []
    horas_totales = 0.0
    
    tot_mod = 0.0
    tot_moi = 0.0
    tot_cif = 0.0
    costo_conversion_total = 0.0
    
    for _, row in tiempos_edit.iterrows():
        proc = row["Proceso"]
        tarifas_p = tarifas_dict.get(proc, {"Costo Mano de Obra Directa": 0, "Costo Mano de Obra Indirecta": 0, "Costos Indirectos de Fabricación": 0, "Total ($/hr)": 0})
        
        hrs_etapa = row[col_t] * row["Multiplicador"] * km
        c_mod = hrs_etapa * tarifas_p["Costo Mano de Obra Directa"]
        c_moi = hrs_etapa * tarifas_p["Costo Mano de Obra Indirecta"]
        c_cif = hrs_etapa * tarifas_p["Costos Indirectos de Fabricación"]
        c_tot_etapa = hrs_etapa * tarifas_p["Total ($/hr)"]
        
        horas_totales += hrs_etapa
        tot_mod += c_mod
        tot_moi += c_moi
        tot_cif += c_cif
        costo_conversion_total += c_tot_etapa
        
        tiempos_detalle.append({
            "Etapa": row["Etapa / Máquina"],
            "Proceso": proc,
            "Horas": hrs_etapa,
            "Tarifa_Hr": tarifas_p["Total ($/hr)"],
            "MOD": c_mod,
            "MOI": c_moi,
            "CIF": c_cif,
            "Costo_Total_Etapa": c_tot_etapa
        })
        
    costo_gran_total = costo_mp_total + costo_conversion_total
    costo_por_metro = costo_gran_total / metros
    
    df_mp = pd.DataFrame([
        {"Materia Prima": "ALAMBRE DE ALUMINIO 1350 9.50 MM H14", "Kg/Km Cable": kg_km_1350, "Consumo Total (kg)": tot_kg_1350, "Costo Total ($)": costo_tot_1350},
        {"Materia Prima": "ALAMBRE DE ALUMINIO 6201 3.00 MM", "Kg/Km Cable": kg_km_6201, "Consumo Total (kg)": tot_kg_6201, "Costo Total ($)": costo_tot_6201},
        {"Materia Prima": "XLPE NEG (2 Fases + 1 Neutro)", "Kg/Km Cable": kg_km_xlpe, "Consumo Total (kg)": tot_kg_xlpe, "Costo Total ($)": costo_tot_xlpe},
    ])
    
    return {
        "df_mp": df_mp,
        "df_tiempos": pd.DataFrame(tiempos_detalle),
        "peso_total": peso_total_kg,
        "costo_mp": costo_mp_total,
        "horas_totales": horas_totales,
        "tot_mod": tot_mod,
        "tot_moi": tot_moi,
        "tot_cif": tot_cif,
        "costo_conv": costo_conversion_total,
        "costo_total": costo_gran_total,
        "costo_metro": costo_por_metro,
        "kg_xlpe": tot_kg_xlpe,
        "costo_xlpe": costo_tot_xlpe
    }

act = calcular_escenario("Actual")
comp = calcular_escenario("Compactado")

diff_costo_tot = comp["costo_total"] - act["costo_total"]
diff_pct_tot = (diff_costo_tot / act["costo_total"]) * 100 if act["costo_total"] > 0 else 0
diff_xlpe_kg = comp["kg_xlpe"] - act["kg_xlpe"]
diff_xlpe_usd = comp["costo_xlpe"] - act["costo_xlpe"]
diff_horas = comp["horas_totales"] - act["horas_totales"]
diff_conv = comp["costo_conv"] - act["costo_conv"]

# 5. TARJETAS DE IMPACTO EJECUTIVO (KPIs)
st.subheader(f"📊 Resultados de Simulación para {metros:,} metros ({km:,.2f} km)")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "💰 Costo Total: RECETA ACTUAL",
    f"${act['costo_total']:,.2f}",
    f"${act['costo_metro']:,.4f} / metro",
    delta_color="off"
)

k2.metric(
    "🚀 Costo Total: COMPACTADO",
    f"${comp['costo_total']:,.2f}",
    f"{diff_costo_tot:+,.2f} ({diff_pct_tot:+.2f}%)",
    delta_color="inverse"
)

k3.metric(
    "🛢️ Ahorro en XLPE NEG",
    f"{abs(diff_xlpe_kg):,.2f} kg",
    f"{diff_xlpe_usd:+,.2f} USD en aislamiento",
    delta_color="inverse"
)

k4.metric(
    "⏱️ Tiempo y Costo de Conversión",
    f"{comp['horas_totales']:,.2f} hrs",
    f"{diff_horas:+,.2f} hrs ({diff_conv:+,.2f} USD)",
    delta_color="inverse"
)

st.divider()

# 6. CONTENIDO DEL RESTO DE PESTAÑAS
with tab1:
    st.markdown("### Desglose de Materia Prima (2 Fases ASC + 1 Neutro AAAC)")
    
    df_comp_mp = pd.DataFrame({
        "Materia Prima": act["df_mp"]["Materia Prima"],
        "Actual (kg/km)": act["df_mp"]["Kg/Km Cable"],
        "Compactado (kg/km)": comp["df_mp"]["Kg/Km Cable"],
        "Consumo Actual (kg)": act["df_mp"]["Consumo Total (kg)"],
        "Consumo Compactado (kg)": comp["df_mp"]["Consumo Total (kg)"],
        "Costo Actual ($)": act["df_mp"]["Costo Total ($)"],
        "Costo Compactado ($)": comp["df_mp"]["Costo Total ($)"],
        "Diferencia ($)": comp["df_mp"]["Costo Total ($)"] - act["df_mp"]["Costo Total ($)"]
    })
    
    st.dataframe(
        df_comp_mp.style.format({
            "Actual (kg/km)": "{:,.2f}",
            "Compactado (kg/km)": "{:,.2f}",
            "Consumo Actual (kg)": "{:,.2f}",
            "Consumo Compactado (kg)": "{:,.2f}",
            "Costo Actual ($)": "${:,.2f}",
            "Costo Compactado ($)": "${:,.2f}",
            "Diferencia ($)": "${:+,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

with tab2:
    st.markdown("### Tiempos por Etapa y Desglose de Costos (MOD + MOI + CIF)")
    
    df_comp_t = pd.DataFrame({
        "Etapa / Máquina": act["df_tiempos"]["Etapa"],
        "Proceso": act["df_tiempos"]["Proceso"],
        "Tarifa ($/hr)": act["df_tiempos"]["Tarifa_Hr"],
        "Horas Actual": act["df_tiempos"]["Horas"],
        "Horas Compactado": comp["df_tiempos"]["Horas"],
        "Costo Actual ($)": act["df_tiempos"]["Costo_Total_Etapa"],
        "Costo Compactado ($)": comp["df_tiempos"]["Costo_Total_Etapa"],
        "Dif. Costo ($)": comp["df_tiempos"]["Costo_Total_Etapa"] - act["df_tiempos"]["Costo_Total_Etapa"]
    })
    
    st.dataframe(
        df_comp_t.style.format({
            "Tarifa ($/hr)": "${:,.2f}",
            "Horas Actual": "{:,.2f}",
            "Horas Compactado": "{:,.2f}",
            "Costo Actual ($)": "${:,.2f}",
            "Costo Compactado ($)": "${:,.2f}",
            "Dif. Costo ($)": "${:+,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("#### Resumen Acumulado de Conversión (Todas las etapas)")
    df_res_conv = pd.DataFrame([
        {"Rubro": "Costo Mano de Obra Directa (MOD)", "Actual ($)": act["tot_mod"], "Compactado ($)": comp["tot_mod"], "Diferencia ($)": comp["tot_mod"] - act["tot_mod"]},
        {"Rubro": "Costo Mano de Obra Indirecta (MOI)", "Actual ($)": act["tot_moi"], "Compactado ($)": comp["tot_moi"], "Diferencia ($)": comp["tot_moi"] - act["tot_moi"]},
        {"Rubro": "Costos Indirectos de Fabricación (CIF)", "Actual ($)": act["tot_cif"], "Compactado ($)": comp["tot_cif"], "Diferencia ($)": comp["tot_cif"] - act["tot_cif"]},
        {"Rubro": "TOTAL COSTOS DE CONVERSIÓN", "Actual ($)": act["costo_conv"], "Compactado ($)": comp["costo_conv"], "Diferencia ($)": comp["costo_conv"] - act["costo_conv"]},
    ])
    st.dataframe(
        df_res_conv.style.format({
            "Actual ($)": "${:,.2f}",
            "Compactado ($)": "${:,.2f}",
            "Diferencia ($)": "${:+,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

with tab4:
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("**Comparación de Costo Total por Rubro ($)**")
        df_bar = pd.DataFrame([
            {"Rubro": "Aluminio 1350 (Fases)", "Escenario": "Actual", "Costo ($)": act["df_mp"].loc[0, "Costo Total ($)"]},
            {"Rubro": "Aluminio 1350 (Fases)", "Escenario": "Compactado", "Costo ($)": comp["df_mp"].loc[0, "Costo Total ($)"]},
            {"Rubro": "Aluminio 6201 (Neutro)", "Escenario": "Actual", "Costo ($)": act["df_mp"].loc[1, "Costo Total ($)"]},
            {"Rubro": "Aluminio 6201 (Neutro)", "Escenario": "Compactado", "Costo ($)": comp["df_mp"].loc[1, "Costo Total ($)"]},
            {"Rubro": "XLPE NEG (Aislamiento)", "Escenario": "Actual", "Costo ($)": act["df_mp"].loc[2, "Costo Total ($)"]},
            {"Rubro": "XLPE NEG (Aislamiento)", "Escenario": "Compactado", "Costo ($)": comp["df_mp"].loc[2, "Costo Total ($)"]},
            {"Rubro": "MOD + MOI + CIF", "Escenario": "Actual", "Costo ($)": act["costo_conv"]},
            {"Rubro": "MOD + MOI + CIF", "Escenario": "Compactado", "Costo ($)": comp["costo_conv"]},
        ])
        fig_bar = px.bar(
            df_bar, x="Rubro", y="Costo ($)", color="Escenario", barmode="group",
            color_discrete_map={"Actual": "#EF553B", "Compactado": "#00CC96"}
        )
        fig_bar.update_layout(xaxis_title="", legend_title="")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_g2:
        st.markdown("**Consumo de XLPE NEG: Actual vs. Compactado (kg)**")
        df_xlpe_g = pd.DataFrame([
            {"Escenario": "Receta Actual", "Consumo XLPE (kg)": act["kg_xlpe"]},
            {"Escenario": "Receta Compactada", "Consumo XLPE (kg)": comp["kg_xlpe"]}
        ])
        fig_xlpe = px.bar(
            df_xlpe_g, x="Escenario", y="Consumo XLPE (kg)", color="Escenario", text_auto=".2f",
            color_discrete_map={"Receta Actual": "#EF553B", "Receta Compactada": "#00CC96"}
        )
        fig_xlpe.update_layout(xaxis_title="", showlegend=False)
        st.plotly_chart(fig_xlpe, use_container_width=True)
