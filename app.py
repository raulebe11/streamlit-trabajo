import streamlit as st
import pandas as pd
import plotly.express as px

# Configuracion de pagina
st.set_page_config(
    page_title="Dashboard Ventas",
    layout="wide"
)

# Cargar de datos
df1 = pd.read_csv('parte_1.csv')
df2 = pd.read_csv('parte_2.csv')
df = pd.concat([df1, df2], ignore_index=True)
df['date'] = pd.to_datetime(df['date'])

st.title("Dashboard de Ventas")

# Pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "Vision Global",
    "Por Tienda", 
    "Por Estado",
    "Insights"
])

# Pestaña 1
with tab1:
    st.header("Vision Global de Ventas")
    
    # a) Conteo General
    st.subheader("a) Conteo General")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tiendas", df['store_nbr'].nunique())
    with col2:
        st.metric("Total Productos", df['family'].nunique())
    with col3:
        st.metric("Estados", df['state'].nunique())
    with col4:
        st.metric("Meses con Datos", df.groupby(['year', 'month']).ngroups)
    
    st.divider()
    
    # b) Analisis en Terminos Medios
    st.subheader("b) Analisis en Terminos Medios")
    
    # i. Top 10 productos mas vendidos
    st.write("**i. Ranking Top 10 Productos Mas Vendidos**")
    top_productos = df.groupby('family')['sales'].mean().sort_values(ascending=True).tail(10)
    fig1 = px.bar(
        x=top_productos.values,
        y=top_productos.index,
        orientation='h',
        title='Top 10 Productos por Ventas Promedio'
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    # ii. Distribucion de ventas por tiendas
    with col1:
        st.write("**ii. Distribucion de Ventas por Tiendas**")
        ventas_tienda = df.groupby('store_nbr')['sales'].sum()
        fig2 = px.pie(
            values=ventas_tienda.values,
            names=ventas_tienda.index,
            title='Distribucion de Ventas por Tienda'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # iii. Top 10 tiendas con ventas en promocion
    with col2:
        st.write("**iii. Top 10 Tiendas con Ventas en Promocion**")
        df_promo = df[df['onpromotion'] > 0]
        top_promo = df_promo.groupby('store_nbr')['sales'].mean().sort_values(ascending=True).tail(10)
        fig3 = px.bar(
            x=top_promo.values,
            y=top_promo.index,
            orientation='h',
            title='Top 10 Tiendas en Promocion'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    st.divider()
    
    # c) Analisis de Estacionalidad
    st.subheader("c) Analisis de Estacionalidad")
    
    col1, col2, col3 = st.columns(3)
    
    # i. Ventas por dia de la semana
    with col1:
        st.write("**i. Ventas por Dia de la Semana**")
        ventas_dia = df.groupby('day_of_week')['sales'].mean()
        fig4 = px.bar(
            x=ventas_dia.index, 
            y=ventas_dia.values,
            title='Ventas Promedio por Dia'
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # ii. Ventas por semana del año
    with col2:
        st.write("**ii. Ventas por Semana del Año**")
        ventas_semana = df.groupby('week')['sales'].mean().sort_index()
        fig5 = px.line(
            x=ventas_semana.index, 
            y=ventas_semana.values,
            title='Ventas Promedio por Semana'
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    # iii. Ventas por mes
    with col3:
        st.write("**iii. Ventas por Mes**")
        ventas_mes = df.groupby('month')['sales'].mean()
        fig6 = px.bar(
            x=ventas_mes.index, 
            y=ventas_mes.values,
            title='Ventas Promedio por Mes'
        )
        st.plotly_chart(fig6, use_container_width=True)


# Pestaña 2

with tab2:
    st.header("Analisis por Tienda")
    
    # Desplegable para elegir tienda
    lista_tiendas = sorted(df['store_nbr'].unique())
    tienda = st.selectbox(
        'Elige la tienda que quieres analizar',
        lista_tiendas
    )
    
    df_tienda = df[df['store_nbr'] == tienda]
    
    st.divider()
    
    # a) Ventas por año (ordenado de antiguo a reciente)
    st.write("**a) Numero Total de Ventas por Año**")
    ventas_anio = df_tienda.groupby('year')['sales'].sum().sort_index()
    fig7 = px.bar(
        x=ventas_anio.index,
        y=ventas_anio.values,
        title=f'Ventas Anuales - Tienda {tienda}'
    )
    st.plotly_chart(fig7, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    # b) Numero total de productos vendidos
    with col1:
        st.write("**b) Numero Total de Productos Vendidos**")
        productos_tienda = df_tienda.groupby('family')['sales'].sum().sort_values(ascending=True).tail(10)
        fig8 = px.bar(
            x=productos_tienda.values,
            y=productos_tienda.index,
            orientation='h',
            title='Top 10 Productos'
        )
        st.plotly_chart(fig8, use_container_width=True)
    
    # c) Productos vendidos en promocion
    with col2:
        st.write("**c) Productos Vendidos en Promocion**")
        df_tienda_promo = df_tienda[df_tienda['onpromotion'] > 0]
        productos_promo = df_tienda_promo.groupby('family')['sales'].sum().sort_values(ascending=True).tail(10)
        fig9 = px.bar(
            x=productos_promo.values,
            y=productos_promo.index,
            orientation='h',
            title='Top 10 Productos en Promocion'
        )
        st.plotly_chart(fig9, use_container_width=True)


# Pestaña 3

with tab3:
    st.header("Analisis por Estado")
    
    # Desplegable para elegir estado
    lista_estados = sorted(df['state'].dropna().unique())
    estado = st.selectbox(
        'Selecciona el estado',
        lista_estados
    )
    
    df_estado = df[df['state'] == estado]
    
    st.divider()
    
    # a) Transacciones por año
    st.write("**a) Numero Total de Transacciones por Año**")
    trans_anio = df_estado.groupby('year')['transactions'].sum().sort_index()
    fig10 = px.bar(
        x=trans_anio.index,
        y=trans_anio.values,
        title=f'Transacciones Anuales - {estado}'
    )
    st.plotly_chart(fig10, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    # b) Ranking de tiendas con mas ventas
    with col1:
        st.write("**b) Ranking de Tiendas con Mas Ventas**")
        ranking = df_estado.groupby('store_nbr')['sales'].sum().sort_values(ascending=True).tail(10)
        fig11 = px.bar(
            x=ranking.values,
            y=ranking.index,
            orientation='h',
            title='Top 10 Tiendas del Estado'
        )
        st.plotly_chart(fig11, use_container_width=True)
    
    # c) Producto mas vendido
    with col2:
        st.write("**c) Producto Mas Vendido**")
        productos_estado = df_estado.groupby('family')['sales'].sum().sort_values(ascending=True).tail(10)
        fig12 = px.bar(
            x=productos_estado.values,
            y=productos_estado.index,
            orientation='h',
            title='Top 10 Productos del Estado'
        )
        st.plotly_chart(fig12, use_container_width=True)


# Pestaña 4 - Insights

with tab4:
    st.header("Insights")
    
    # Evolucion temporal
    st.subheader("Evolucion de Ventas")
    ventas_mensuales = df.groupby(['year', 'month'])['sales'].sum().reset_index()
    ventas_mensuales['fecha'] = pd.to_datetime(
        ventas_mensuales['year'].astype(str) + '-' + 
        ventas_mensuales['month'].astype(str).str.zfill(2) + '-01'
    )
    fig13 = px.line(
        ventas_mensuales,
        x='fecha',
        y='sales',
        title='Tendencia de Ventas Mensuales'
    )
    st.plotly_chart(fig13, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    # Impacto promociones
    with col1:
        st.subheader("Impacto de Promociones")
        ventas_sin = df[df['onpromotion'] == 0]['sales'].mean()
        ventas_con = df[df['onpromotion'] > 0]['sales'].mean()
        fig14 = px.bar(
            x=['Sin Promocion', 'Con Promocion'],
            y=[ventas_sin, ventas_con],
            title='Comparativa de Ventas'
        )
        st.plotly_chart(fig14, use_container_width=True)
    
    # Por tipo de tienda
    with col2:
        st.subheader("Ventas por Tipo de Tienda")
        ventas_tipo = df.groupby('store_type')['sales'].mean().sort_values(ascending=True)
        fig15 = px.bar(
            x=ventas_tipo.values,
            y=ventas_tipo.index,
            orientation='h',
            title='Ventas Promedio por Tipo'
        )
        st.plotly_chart(fig15, use_container_width=True)
