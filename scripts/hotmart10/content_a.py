# -*- coding: utf-8 -*-
"""Contenido del playbook - Capítulo 1 + Productos 1 a 5. Sin emoji, español."""

CH1 = {
 "intro": ("Este playbook nace de una conclusión simple: en 2026 los productos de información "
   "(ebooks, packs de prompts, cursos genéricos) se han vuelto imposibles de vender porque la "
   "inteligencia artificial los genera gratis en minutos. Lo que la IA no puede reemplazar es "
   "software funcionando que resuelve un dolor concreto de un negocio real. Cada uno de los diez "
   "productos de este documento es una herramienta con demanda verificada en América Latina, "
   "competidores que ya cobran por resolver ese dolor y un camino técnico realista de construcción "
   "con las habilidades de desarrollo que ya existen en el equipo. Nada aquí depende de tener "
   "audiencia previa: cada capítulo incluye el copy de la landing en el estilo que usan los "
   "líderes de su categoría, la arquitectura técnica y el plan de precios para Hotmart."),
 "metodo": ("La selección obedeció a cuatro filtros aplicados en orden. Primero, dolor frecuente: "
   "el cliente pierde dinero o tiempo todos los días por no tener la herramienta. Segundo, "
   "competencia validada: si nadie cobra por resolver el problema, probablemente nadie lo tiene; "
   "cada capítulo documenta quiénes venden hoy y a qué precio. Tercero, construcción acelerada: "
   "el producto debe salir en dos a seis semanas con Python, FastAPI y un panel web, sin equipos "
   "grandes. Cuarto, distribución en Hotmart: precio de impulso (entre 9 y 99 dólares), comprador "
   "hispanohablante y garantía de siete días. Se descartaron deliberadamente los nichos donde la "
   "IA ya destruyó el valor (información) y los que exigen certificaciones o licencias que el "
   "equipo no posee."),
 "matriz_head": ["Producto", "Cliente objetivo", "Precio Hotmart", "Competencia ancla", "MVP", "Potencial"],
 "matriz": [
   ["1. WAOrder (bot pedidos WhatsApp)", "Tiendas y comida a domicilio", "$19/mes o $97 único", "Whaticket $49/mes", "3 sem.", "Muy alto"],
   ["2. FacturaEC (SRI Ecuador)", "Freelancers y pymes EC", "$39/año", "Dátil $8-34/mes", "4-6 sem.", "Alto"],
   ["3. LeadMiner (leads Instagram)", "Agencias de marketing", "$29/mes", "Apify $1.5/1K", "2 sem.", "Alto"],
   ["4. PriceRadar (precios ML)", "Sellers de marketplace", "$19-39/mes", "Prisync $99/mes", "2-3 sem.", "Alto"],
   ["5. ScamGuard (validador URLs)", "Comercios y desarrolladores", "$9-15/mes", "ScamAdviser", "3 días", "Medio"],
   ["6. CitaYa (reservas WhatsApp)", "Barberías, salones, consultorios", "$14/mes", "AgendaPro $9-59/mes", "3 sem.", "Muy alto"],
   ["7. ReviewReply (reseñas con IA)", "Restaurantes y clínicas", "$24/mes", "Birdeye (enterprise)", "2 sem.", "Alto"],
   ["8. PostFactory (contenido IA)", "Negocios de barrio", "$17/mes", "Predis.ai $29/mes", "3-4 sem.", "Medio-alto"],
   ["9. MenuQR (carta digital)", "Restaurantes y cafeterías", "$11/mes", "Treggio, BuenaCarta", "2 sem.", "Alto"],
   ["10. LicitAlert (SERCOP)", "Proveedores del Estado EC", "$29/mes", "Consultores manuales", "2 sem.", "Nicho sólido"],
 ],
 "matriz_nota": ("La columna MVP estima el tiempo hasta una versión vendible con el stack propuesto. "
   "El potencial combina tamaño del mercado hispano, frecuencia de pago y capacidad real de "
   "distribución desde cero. ScamGuard aparece con el MVP más corto porque ya existe un prototipo "
   "funcional del verificador de fraudes construido previamente; su trabajo pendiente es de "
   "empaquetamiento, no de desarrollo."),
}

PRODUCTS_A = [
{
 "num": 1, "key": "p01_waorder",
 "name": "WAOrder - Bot de pedidos por WhatsApp",
 "tagline": "El bot que convierte el WhatsApp del negocio en una caja registradora",
 "cliente": "Tiendas de barrio, comida a domicilio, ferreterías, farmacias y distribuidoras pequeñas de toda América Latina.",
 "pain": ("El negocio pequeño latinoamericano vive en WhatsApp. Recibe entre veinte y ochenta "
   "mensajes diarios preguntando lo mismo: precio, si hay stock, horarios, cómo pagar. El dueño "
   "atiende, despacha y cobra al mismo tiempo, y cada mensaje sin respuesta en cinco minutos es "
   "una venta que se va a la competencia. Las plataformas multiagente del mercado (Whaticket, "
   "Wati, Callbell) resuelven el problema de equipos grandes con varios empleados contestando, "
   "pero el dueño solo no necesita repartir chats entre agentes: necesita que las preguntas "
   "frecuentes se respondan solas y que el pedido llegue estructurado con producto, cantidad y "
   "dirección. Ahí está el hueco: un bot que atienda solo, cobre dentro del flujo y deje al "
   "humano para lo humano."),
 "market": ("Whaticket confirma el tamaño del mercado con planes desde 49 dólares al mes y una "
   "comunidad enorme en Brasil, Colombia y México; Wati cobra 119 dólares más 39 por usuario "
   "adicional. Entre esas cifras de empresa y el plan gratuito de WhatsApp Business App hay un "
   "desierto: el dueño solo o de dos personas. Ese segmento paga bien entre 15 y 25 dólares "
   "mensuales por automatización que se instala en minutos y no exige configurar flujos."),
 "competitors": [
   ["Whaticket", "Plan fijo por usuarios", "$49-109/mes", "Chatbot por palabras clave, sin IA; foco multiagente"],
   ["Wati", "Suscripción + por usuario", "$119/mes + $39/usuario", "API oficial, potente y caro para pyme"],
   ["Callbell", "Por agente", "$45-60 EUR/mes", "Buena interfaz, analíticas por agente"],
   ["Tecca", "IA resolvente", "desde $24/mes", "El competidor conceptual más cercano; validar su copy"],
 ],
 "estilo": ("El estilo que funciona en esta categoría y que WAOrder debe copiar: precio fijo y "
   "predecible por plan (el argumento central de Whaticket frente al cobro por agente), promesa "
   "de instalación en minutos sin técnicos, demostración en video de un pedido real completo y "
   "tabla comparativa donde el competidor aparece como 'plataforma multiagente para equipos' y "
   "el producto propio como 'el asistente que atiende solo para negocios de uno'. La página de "
   "Tecca demuestra que el ángulo 'menos humanos atendiendo' vende; el copy de la landing lo "
   "adopta como propuesta central."),
 "copy": {
   "headline": "Tu WhatsApp atiende solo y te pasa el pedido listo para despachar",
   "sub": ("WAOrder responde precios y stock al instante, arma el carrito dentro del chat y te "
     "entrega el pedido estructurado con dirección y forma de pago. Sin apps para el cliente, "
     "sin flujos complicados, sin equipo de agentes."),
   "bullets": [
     "Responde precio, stock y horarios solo, 24 horas, en menos de 5 segundos",
     "Arma el pedido con productos, cantidades y dirección dentro del chat",
     "Cobra con link de pago, transferencia o contra entrega, sin salir de WhatsApp",
     "Te avisa por cada pedido nuevo: tú solo despachas y cobras",
     "Guarda cada cliente con su historial para venderle de nuevo",
     "Instalación de 10 minutos con tu número actual; no pierdes tus chats",
   ],
   "para_quien": ("Es para ti si eres dueño de una tienda, comida a domicilio o distribuidora, "
     "atiendes el WhatsApp solo o con una persona y pierdes ventas por mensajes que se quedan "
     "sin responder. No es para call centers con diez agentes: para eso ya existen las "
     "plataformas multiagente."),
   "incluye": ["Bot de pedidos con IA para 1 número de WhatsApp", "Panel de pedidos y clientes en la web",
     "Catálogo ilimitado con fotos y precios", "Links de pago integrados", "Capacitación en video de 20 minutos",
     "Actualizaciones y soporte por el mismo WhatsApp"],
   "garantia": ("Garantía de 7 días de Hotmart: si en una semana el bot no te está ahorrando "
     "mensajes, se devuelve el 100 por ciento sin explicaciones."),
   "faq": [
     ["Necesito un número nuevo o Linea oficial de WhatsApp?", "Funciona con tu número actual mediante WhatsApp Business App en el arranque; cuando el volumen crece, migras a la API oficial con el mismo panel."],
     ["Que pasa si el bot no sabe responder algo?", "Deriva la conversación a ti con el contexto completo del cliente; nunca deja un mensaje colgado."],
     ["Puedo cambiar precios del catalogo yo mismo?", "Si, el panel es tuyo: fotos, precios y disponibilidad se editan en segundos desde el celular."],
   ],
   "cta": "Pruébalo 7 días. Si no te ahorra mensajes, te devuelven todo.",
 },
 "stack": ("Python con FastAPI para el motor de conversación, webhooks de WhatsApp Cloud API "
   "(fase uno puede operar sobre WhatsApp Business App con la librería baileys para arrancar sin "
   "costo de API), base PostgreSQL para catálogos, pedidos y clientes, pasarela local (link de "
   "pago PayPhone en Ecuador o Mercado Pago regional) y panel React ligero. La IA conversacional "
   "se apoya en un modelo económico por API con catálogo inyectado como contexto."),
 "fases": [
   ["Semana 1 - Esqueleto que conversa", "Webhook de WhatsApp, catálogo cargable, respuestas de precio y stock, derivación a humano."],
   ["Semana 2 - Pedido y cobro", "Carrito en chat, confirmación de dirección, link de pago, notificación de pedido nuevo al dueño."],
   ["Semana 3 - Panel y lanzamiento", "Panel web de pedidos y clientes, video demo, landing en Hotmart con 20 cupos fundadores."],
 ],
 "pricing": [
   ["Fundador (primeros 20)", "$67 pago único", "Licencia de por vida del bot + panel; sin costo mensual"],
   ["Estándar", "$19/mes o $97 único", "Todo incluido; actualizaciones continuas"],
   ["Con configuración hecha", "$147 único", "Se carga el catálogo y se deja funcionando por ti"],
 ],
 "launch": ("Lanzar primero con veinte cupos fundadores a 67 dólares único entre negocios del "
   "entorno inmediato (los contactos comerciales de la empresa sirven de primeros clientes y "
   "testimonios), pedir grabación de pantalla del pedido real a cambio de descuento, y usar esas "
   "pruebas en la landing pública de Hotmart. Los grupos de Facebook de emprendedores del país "
   "y las páginas de comida a domicilio son el canal de captación natural."),
 "precio_hotmart": "$19/mes o $97 único", "esfuerzo": "3 semanas", "potencial": "Muy alto",
 "risk": ("Riesgo principal: cambios de política de WhatsApp. Mitigación: arrancar sobre la App "
   "Business con automatización de terceros documentada y ofrecer migración a Cloud API como "
   "mejora de plan, nunca como bloqueo."),
},
{
 "num": 2, "key": "p02_facturaec",
 "name": "FacturaEC - Emisor de facturación electrónica SRI",
 "tagline": "Facturar al SRI en Ecuador sin pagar un sistema contable completo",
 "cliente": "Freelancers, médicos, consultores y pymes ecuatorianas que emiten pocos comprobantes pero necesitan cumplir con el SRI.",
 "pain": ("En Ecuador emitir un comprobante electrónico exige firmar el XML con certificado "
   "digital y autorizarlo en los WebServices del SRI. El mercado respondió con dos extremos: "
   "sistemas contables completos (Dátil, Contifico, Factuplan) que cobran mensualidades crecientes "
   "por funciones de inventario y contabilidad que un freelancer nunca usa, o trámites manuales "
   "en el portal del SRI que consumen horas. Dátil arranca en 8 dólares al mes hasta 60 documentos; "
   "Contifico regala 24 documentos al año para enganchar y luego escala. El hueco real: una "
   "suscripción anual plana y barata, pensada solo para emitir, firmar y entregar comprobantes, "
   "sin contabilidad pegada. El comprador entiende este dolor instantáneamente porque la "
   "obligación tributaria no es opcional."),
 "market": ("El segmento de contribuyentes que emite menos de cien comprobantes al mes es "
   "gigantesco en Ecuador: profesionales independientes que facturan a una o dos empresas, "
   "tiendas de barrio con RIMPE, médicos de consultorio. Una herramienta anual de 39 dólares "
   "compite directamente contra 96 a 408 dólares anuales de los sistemas con mensualidad, y el "
   "argumento de venta es aritmética pura."),
 "competitors": [
   ["Dátil", "Mensual por volumen", "$8-34/mes (60+ docs)", "Líder de marca; API pública para devs"],
   ["Siigo Contifico", "Anual por documentos", "$14-20/año (48 docs)", "Gratis de entrada para enganchar al ecosistema"],
   ["Factuplan", "Mensual", "desde $49/mes", "Foco empresarial con soporte"],
   ["Quipuy", "Anual low-cost", "desde $6/año", "Precios agresivos; validar su alcance funcional"],
 ],
 "estilo": ("Dátil vende con una página de planes limpia organizada por volumen de documentos "
   "('planes para todo tipo de empresas') y credenciales técnicas (documentación para "
   "desarrolladores). Contifico engancha con el plan gratuito de documentos. FacturaEC copia las "
   "dos tácticas: tabla de planes por volumen con el plan de entrada protagonista y una primera "
   "tanda de comprobantes de cortesía para probar el flujo completo antes de pagar. El mensaje "
   "central del copy es de cumplimiento sin fricción: 'autorizado por el SRI en segundos, "
   "archivado y enviado a tu cliente sin que toques el portal'."),
 "copy": {
   "headline": "Emite facturas autorizadas por el SRI en 30 segundos, desde 39 dólares AL ANO",
   "sub": ("FacturaEC firma tu comprobante con tu certificado digital, lo autoriza en el SRI, "
     "guarda el XML y manda el PDF a tu cliente. Sin mensualidades de sistema contable que no "
     "usas: solo facturar, cumplir y seguir trabajando."),
   "bullets": [
     "Facturas, notas de crédito y débito, retenciones y guías de remisión",
     "Firma electrónica con tu certificado .p12 en dos clics",
     "Autorización automática en los WebServices del SRI con reintentos",
     "XML y PDF archivados y descargables para siempre",
     "Envío automático al cliente por email o WhatsApp",
     "Precio anual plano: sin sorpresas por documento o por usuario",
   ],
   "para_quien": ("Es para profesionales independientes y negocios pequeños que emiten hasta cien "
     "comprobantes al mes y no quieren pagar un sistema contable completo. Si llevas contabilidad "
     "con contador externo, FacturaEC se integra perfectamente: tu contador sigue con lo suyo y "
     "tú solo emites."),
   "incluye": ["Emisor web de todos los comprobantes SRI vigentes", "Firma con certificado .p12",
     "Cola de autorización con reintentos automáticos", "Archivo permanente de XML y PDF",
     "Base de clientes y productos con importación masiva", "Soporte por WhatsApp en horario laboral"],
   "garantia": ("Garantía de 7 días: emite tus primeros comprobantes reales; si el flujo no te "
     "resulta más rápido que lo que usas hoy, devolución total."),
   "faq": [
     ["Funciona con RIMPE?", "Si, emite comprobantes para contribuyentes RIMPE Emprendedor y RIMPE Régimen General con su numeración correspondiente."],
     ["Necesito firma electrónica?", "Si, la firma .p12 es obligatoria según el SRI; si no la tienes, el soporte te guía para comprarla en las entidades autorizadas."],
     ["Que pasa si el SRI esta caido?", "El sistema guarda el comprobante firmado y reintenta solo hasta autorizarlo; nunca pierdes un documento."],
   ],
   "cta": "Paga una vez al año. Factura todo el año sin pensar en el SRI.",
 },
 "stack": ("FastAPI con un worker de cola (Redis o RQ) para emisión y reintentos; generación y "
   "firma XAdES del XML en Python (librería xmlsec o firma externalizada en un microservicio con "
   "openssl); integración directa con los WebServices de recepción y autorización del SRI; "
   "almacenamiento S3-compatible para XML/PDF; panel React. Certificado del cliente gestionado "
   "con cifrado en reposo."),
 "fases": [
   ["Semanas 1-2 - Núcleo de emisión", "Modelado de comprobantes, generación XML por tipo, firma XAdES, prueba en ambiente de homologación del SRI."],
   ["Semanas 3-4 - Ciclo completo", "Autorización con reintentos, archivo, envío al cliente, importación CSV, panel responsive."],
   ["Semanas 5-6 - Endurecimiento", "Manejo de errores SRI reales, validación RUC, video demo, beta con 10 freelancers reales antes de publicar."],
 ],
 "pricing": [
   ["Prueba", "gratis", "5 comprobantes de cortesía para validar el flujo completo"],
   ["Anual plano", "$39/año", "Hasta 200 comprobantes al mes, todos los tipos"],
   ["Contador (multi-cliente)", "$89/año", "Hasta 10 RUC gestionados desde un solo panel"],
 ],
 "launch": ("El regulador exige precisión: antes de vender, dos semanas de beta gratuita con "
   "diez freelancers reales emitiendo comprobantes reales, capturando cada error de homologación. "
   "El canal de distribución más barato son los contadores (el plan multi-cliente les sirve para "
   "gestionar clientes) y los grupos de Facebook de emprendedores ecuatorianos, donde el dolor "
   "SRI se queja a diario. Publicar la herramienta también en un directorio propio con guía "
   "'cómo emitir tu primera factura electrónica' posiciona el SEO local desde el día uno."),
 "precio_hotmart": "$39/año", "esfuerzo": "4-6 semanas", "potencial": "Alto",
 "risk": ("Riesgo regulatorio: cambios de esquema XML o del servicio de autorización. Mitigación: "
   "suscripción anual renueva cada doce meses, dando ventana natural para adaptar sin renegotiar "
   "con el cliente, y el homologador del SRI es estable desde hace años."),
},
{
 "num": 3, "key": "p03_leadminer",
 "name": "LeadMiner - Extractor de leads de Instagram",
 "tagline": "Listas de prospectos calificados de Instagram, listas para tu agencia",
 "cliente": "Agencias de marketing, gestores de anuncios y freelancers de prospección B2C en español.",
 "pain": ("Una agencia que vende servicios a negocios locales necesita prospectos: quién anuncia, "
   "quién no, quién tiene email público, quién responde DMs. Hacerlo a mano son horas de scroll. "
   "Las herramientas internacionales (Apify con actores desde 1.50 dólares por cada mil "
   "resultados, PhantomBuster desde unos 56 dólares mensuales) son técnicas, en inglés y cobran "
   "por consumo técnico que una agencia pequeña no sabe presupuestar. El hueco: un producto en "
   "español con créditos simples incluidos, filtros listos (país, nicho, tamaño) y exportación "
   "directa a la hoja de cálculo donde la agencia ya trabaja. La venta no es 'scraping', es "
   "'agenda llena de reuniones'."),
 "market": ("Latinoamérica está saturada de agencias pequeñas de dos a cinco personas que viven "
   "de captar clientes locales. Es un comprador que ya paga por herramientas de prospección y "
   "entiende el valor de una lista limpia. El precio de ancla es el tiempo: una lista de doscientos "
   "prospectos calificados vale lo que dos días de trabajo manual."),
 "competitors": [
   ["Apify (actores IG)", "Pay por resultado", "$0.20-1.50/1K resultados", "Potente, técnico, en inglés"],
   ["PhantomBuster", "Suscripción por horas", "desde ~$56/mes", "Multi-red, curva de aprendizaje alta"],
   ["Paneles locales de leads", "Mensual fijo", "$20-50/mes", "Calidad de datos irregular"],
 ],
 "estilo": ("Apify vende con precio por mil resultados y plan gratuito; su lección es la "
   "transparencia de precio por unidad. PhantomBuster vende flujos ('phantoms') prearmados: la "
   "táctica copiable es vender 'misiones' ya configuradas en lugar de opciones infinitas. El "
   "copy de LeadMiner ancla todo en el resultado: 'el lunes subes la lista, el viernes tienes "
   "tres reuniones'. Evita deliberadamente la jerga de scraping y muestra la hoja de cálculo "
   "final como imagen de producto."),
 "copy": {
   "headline": "200 leads de Instagram con email y teléfono, en 10 minutos y en español",
   "sub": ("Elige el nicho y la ciudad, y LeadMiner te entrega la lista lista para tu CRM: "
     "negocios activos, con audiencia real y datos de contacto visibles. Sin configurar robots, "
     "sin ingles, sin pagar por cada millar de resultados."),
   "bullets": [
     "Extrae perfiles por hashtag, ubicación, seguidores de tu competencia y sugeridos",
     "Email y teléfono públicos de la bio, más sitio web y tamaño de audiencia",
     "Filtros listos: país, ciudad, nicho, rango de seguidores y actividad reciente",
     "Scoring de lead: quién anuncia hoy, quién responde, quién crece",
     "Export directo a CSV, Google Sheets o tu CRM",
     "Créditos mensuales incluidos: sabes exactamente cuánto pagas",
   ],
   "para_quien": ("Es para agencias de 1 a 10 personas y prospectores que venden a negocios "
     "locales y necesitan listas nuevas cada semana. No es para spamear: los datos son públicos "
     "y la herramienta existe para abrir conversaciones comerciales legítimas."),
   "incluye": ["Créditos mensuales de extracción renovables", "Misiones prearmadas por objetivo",
     "Filtros y scoring automáticos", "Export CSV / Sheets / webhook", "Plantillas de primer mensaje de contacto",
     "Soporte en español"],
   "garantia": ("Garantía de 7 días: si tu primera lista no trae datos utilizables, devolución "
     "completa."),
   "faq": [
     ["Es legal usar estos datos?", "Se procesan unicamente datos publicos de perfiles de negocios, con limites de tasa para respetar la plataforma; la herramienta esta pensada para prospeccion comercial legitima."],
     ["Cuantos leads saco por mes?", "El plan incluye creditos para aprox. 5,000 perfiles procesados al mes; los creditos no usados se acumulan."],
     ["Necesito saber de tecnologia?", "No: eliges la mision (nicho + ciudad), presionas ejecutar y descargas la lista."],
   ],
   "cta": "Tu próxima lista de clientes está a 10 minutos. Pruébalo 7 días.",
 },
 "stack": ("Trabajadores Python con Playwright e instagrapi sobre colas; pool de proxies "
   "residenciales rotativos con presupuesto de tasa por sesión; enriquecimiento con parseo de "
   "bio y detección de contacto; PostgreSQL para histórico de perfiles y deduplicación; panel "
   "Next.js con la vista de lista y filtros; exportación a Sheets vía API."),
 "fases": [
   ["Semana 1 - Extracción base", "Actores de perfil, hashtag y seguidores; tasa segura; almacén de perfiles."],
   ["Semana 2 - Producto vendible", "Enriquecimiento, filtros, scoring, export, panel simple, landing y 10 listas gratis para agencias amigas."],
 ],
 "pricing": [
   ["Agencia", "$29/mes", "Créditos para ~5,000 perfiles/mes, filtros y scoring completos"],
   ["Pro", "$49/mes", "Créditos para ~15,000 perfiles, misiones ilimitadas, webhook"],
   ["Anual", "$149/año", "Plan Agencia congelado por 12 meses"],
 ],
 "launch": ("Diez listas de regalo para agencias del entorno con una condición: si la lista sirve, "
   "un testimonio y una captura para la landing. Los grupos de 'agencias de marketing' y las "
   "comunidades de freelance en español son el canal. El argumento de venta se demuestra en el "
   "primer contacto: enviar junto al pitch una mini-lista de diez leads del nicho del prospecto "
   "convierte la venta de confianza en venta de evidencia."),
 "precio_hotmart": "$29/mes", "esfuerzo": "2 semanas", "potencial": "Alto",
 "risk": ("Riesgo operativo: bloqueos de plataforma. Mitigación: rotación de sesiones, ritmo "
   "humano y desacople entre el motor (que puede migrar de proveedor de proxies) y el producto "
   "que ve el cliente."),
},
{
 "num": 4, "key": "p04_priceradar",
 "name": "PriceRadar - Monitor de precios para MercadoLibre",
 "tagline": "Vigila a tus rivales de marketplace y reprecia antes que ellos",
 "cliente": "Sellers de MercadoLibre y Amazon de habla hispana con catálogos de 20 a 500 productos.",
 "pain": ("El seller de marketplace compite a ciegas: el rival baja precio a las tres de la tarde "
   "y a las seis ya le robaron la venta Buy Box o el posicionamiento. Las herramientas globales "
   "(Prisync desde 99 dólares al mes por cien productos, Priceva orientada a empresa) están "
   "pensadas para catálogos europeos o norteamericanos y sus precios se comen el margen de un "
   "vendedor mediano latinoamericano. El hueco es evidente: monitorización enfocada en "
   "MercadoLibre, alertas donde el seller ya vive (Telegram y WhatsApp), y precios de 19 a 39 "
   "dólares. La promesa se demuestra con una cifra: sostener el precio correcto frente a la "
   "competencia mueve el margen entre 3 y 20 por ciento, que es exactamente el argumento que "
   "Prisync usa para justificar sus 99 dólares."),
 "market": ("El universo de sellers hispanohablantes en MercadoLibre se cuenta en cientos de "
   "miles. Es un comprador acostumbrado a pagar por herramientas (etiquetas, reposición, "
   "publicaciones) y acostumbrado a decisiones por retorno inmediato. La venta se cierra cuando "
   "el seller ve la primera alerta de 'tu rival bajó 8 por ciento' detectada antes que por él."),
 "competitors": [
   ["Prisync", "Mensual por productos", "$99-399/mes", "Global, potente, caro para LATAM"],
   ["Priceva", "Enterprise", "Cotización", "Orientado a marcas y distribuidores"],
   ["Hojas de cálculo manuales", "Tiempo humano", "$0 + horas", "El competidor real del segmento"],
 ],
 "estilo": ("Prisync estructura su venta en tres planes por volumen con prueba gratuita de 14 "
   "días sin tarjeta y el argumento del margen mejorado. PriceRadar copia la estructura por "
   "volúmenes ajustados al seller latino (50, 300 y mil productos), la prueba sin tarjeta y el "
   "copy de margen, pero cambia el elemento diferencial de la página: la captura de una alerta "
   "real de Telegram, porque el seller entiende en un segundo qué significa no enterarse a "
   "tiempo."),
 "copy": {
   "headline": "El rival bajó precio a las 15:00. Tu alerta llegó a las 15:01.",
   "sub": ("PriceRadar vigila las publicaciones de tu competencia en MercadoLibre y Amazon, te "
     "avisa al instante en Telegram y te muestra el histórico para repreciar con datos y no con "
     "corazonadas."),
   "bullets": [
     "Vigila ilimitados rivales por cada producto tuyo",
     "Alertas instantáneas de baja de precio y quiebre de stock",
     "Histórico visual de precios por publicación rival",
     "Índice de posición: qué tan caro o barato estás hoy",
     "Match automático producto propio contra competencia",
     "Reporte semanal de movimientos del mercado en tu categoría",
   ],
   "para_quien": ("Es para sellers con catálogo propio que compiten por precio en marketplace y "
     "hoy vigilan rivales a mano. No es para dropshippers sin control de precio."),
   "incluye": ["Hasta 50 / 300 productos según plan", "Alertas Telegram y email",
     "Histórico completo de precios y stock", "Dashboard de índice competitivo",
     "Reporte semanal automático", "Soporte en español"],
   "garantia": ("Garantía de 7 días conectada a tu primer lote de rivales: si la primera semana "
     "no descubres un movimiento que valga la pena, devolución total."),
   "faq": [
     ["Como empareja mis productos con los rivales?", "Subes las URLs de la competencia o dejas que el match automatico sugiera rivales por titulo y categoria; tu confirmas con un clic."],
     ["Cada cuanto actualiza precios?", "Cada 3 horas en plan Inicial y cada hora en plan Growth."],
     ["Funciona para otras plataformas?", "MercadoLibre y Amazon al lanzar; Shopify y Tiendanube en el roadmap."],
   ],
   "cta": "Deja de vigilar a mano. Tu primera alerta llega hoy mismo.",
 },
 "stack": ("Crawler Python (Scrapy/Playwright) con parsers dedicados por marketplace y respaldo "
   "en APIs públicas cuando existen; scheduler con ventanas de rastreo por plan; PostgreSQL con "
   "series temporales simplificadas para histórico; match por similitud de título + confirmación "
   "humana; bot de Telegram y envío de email transaccional; dashboard Next.js con gráficas."),
 "fases": [
   ["Semana 1 - Crawler y match", "Parser de MercadoLibre estable, carga de URLs rivales, match con confirmación."],
   ["Semana 2 - Alertas", "Detección de cambios, bot de Telegram, email semanal, histórico básico."],
   ["Semana 3 - Dashboard y venta", "Índice competitivo, planes por volumen, beta con 10 sellers del entorno."],
 ],
 "pricing": [
   ["Inicial", "$19/mes", "50 productos, alertas cada 3 horas, Telegram + email"],
   ["Growth", "$39/mes", "300 productos, alertas cada hora, histórico completo"],
   ["Anual", "$149/año", "Plan Growth congelado 12 meses"],
 ],
 "launch": ("Reclutar los diez primeros sellers en grupos de Facebook de 'vendedores de "
   "MercadoLibre' ofreciendo la semana de prueba conectada a sus rivales reales; la captura de "
   "'tu rival bajó y tú ya lo sabías' es el activo de marketing más valioso del lanzamiento. El "
   "reporte semanal gratuito del mercado de una categoría (por ejemplo, celulares usados en "
   "Quito) funciona como lead magnet en grupos y foros de sellers."),
 "precio_hotmart": "$19-39/mes", "esfuerzo": "2-3 semanas", "potencial": "Alto",
 "risk": ("Riesgo técnico: cambios de estructura en el sitio del marketplace. Mitigación: "
   "parsers aislados por sitio con tests ante cada despliegue y alerta interna de falla de "
   "parseo antes de que la afecte al cliente."),
},
{
 "num": 5, "key": "p05_scamguard",
 "name": "ScamGuard - Validador de URLs y tiendas falsas",
 "tagline": "El veredicto de confianza que tu sitio, tu app o tu banco puede mostrar",
 "cliente": "Comercios que quieren demostrar que son reales, desarrolladores que integran verificación, y medios o comunidades que denuncian fraudes.",
 "pain": ("El fraude digital en español explota: tiendas falsas que clonan marcas, 'vendedores' "
   "de WhatsApp con precios imposibles, phishing bancario. Las herramientas gratuitas existentes "
   "(ScamAdviser, Google Safe Browsing, VirusTotal) están en inglés, entregan un veredicto "
   "técnico y no ofrecen nada que un negocio legítimo pueda exhibir. Este producto ya existe "
   "como prototipo funcional en el portafolio del equipo: un verificador de fraudes con motor "
   "de señales (edad del dominio, listas negras, SSL, similitud de marca) y scoring explicado. "
   "El trabajo aquí es de empaquetamiento: dos lados de la misma moneda. Para el público, el "
   "chequeo gratis como imán de usuarios. Para el negocio legítimo, un badge verificable que "
   "muestran para vender más. Para el desarrollador o fintech, una API de veredictos."),
 "market": ("El modelo de monetización es de dos caras: el badge mensual para comercios (9 "
   "dólares) convierte el miedo al fraude en un producto de marketing para el comercio honesto, "
   "y la API (15 dólares mensuales por plan inicial) vende a desarrolladores y plataformas que "
   "necesitan veredicto en línea. ScamAdviser valida el modelo con años de tráfico orgánico "
   "monetizado."),
 "competitors": [
   ["ScamAdviser", "Freemium + API", "Gratis al público; API B2B", "Líder global; inglés; veredicto tipo cuadro"],
   ["Google Safe Browsing", "Gratuito", "$0", "Binario (mal/no mal), sin scoring explicable"],
   ["VirusTotal URL", "Freemium", "$0 - planes", "Técnico, orientado a seguridad"],
 ],
 "estilo": ("ScamAdviser gana con simplicidad brutal: una caja de texto enorme, un veredicto "
   "instantáneo y contenido SEO por cada dominio analizado (cada URL consultada genera una "
   "página indexable). Esa táctica de SEO programático es la lección central a copiar: cada "
   "dominio verificado se convierte en una página pública con veredicto y evidencia, atrayendo "
   "tráfico gratis de gente que acaba de dudar de un sitio. El badge copia la dinámica probada "
   "de sellos de confianza clásicos del comercio electrónico."),
 "copy": {
   "headline": "Verifica cualquier tienda online en 3 segundos y evita que te estafen",
   "sub": ("ScamGuard analiza la URL con más de veinte señales reales (antigüedad del dominio, "
     "listas negras, certificados, imitación de marcas) y te da un veredicto claro con evidencia. "
     "Y si tu tienda es legítima, muestra el badge verificable que tus clientes buscan."),
   "bullets": [
     "Veredicto en segundos: seguro, dudoso o fraude, con evidencia punto por punto",
     "Más de veinte señales combinadas con scoring explicable 0-100",
     "Badge verificable para tu sitio si eres un comercio real",
     "API para integrar el veredicto en tu app o plataforma",
     "Historial público por dominio: la gente llega buscando si confiar",
     "Funciona desde el celular, sin instalar nada",
   ],
   "para_quien": ("Para cualquiera que dudó de una tienda antes de pagar. Para comercios legítimos "
     "que quieren demostrarlo. Para desarrolladores y plataformas que necesitan el veredicto por "
     "API."),
   "incluye": ["Verificador público ilimitado", "Reporte con evidencia por URL",
     "Badge verificable (plan comercio)", "API con cuota mensual (plan dev)",
     "Alertas cuando un dominio reportado cambia de dueño", "Soporte en español"],
   "garantia": ("El chequeo es gratis; los planes de pago tienen la garantía estándar de 7 días "
     "de Hotmart."),
   "faq": [
     ["Como gana dinero si el chequeo es gratis?", "El chequeo publico atrae trafico; el dinero esta en el badge para comercios legítimos y en la API para plataformas."],
     ["Que pasa si un sitio legitimo sale como dudoso?", "Todo veredicto incluye un formulario de apelación con revisión manual en 24 horas."],
     ["Puedo integrarlo en mi plataforma?", "Si, la API devuelve el scoring y las señales en JSON con documentación en español."],
   ],
   "cta": "Dudaste de un sitio? Verifícalo ahora, gratis.",
 },
 "stack": ("El prototipo existente (verificador en navegador) se refactoriza a FastAPI con "
   "workers de análisis asíncronos; módulos de señales: WHOIS, Safe Browsing, listas de phishing "
   "públicas, certificado TLS, hash visual del sitio contra clones conocidos y similitud de "
   "marca; scoring ponderado documentado; base PostgreSQL con páginas programáticas por dominio "
   "(SSR para SEO); widget embebible y API con llaves y cuotas."),
 "fases": [
   ["Días 1-3 - Empaquetado", "Migrar el prototipo a API + web pública, veredicto con evidencia, página programática por dominio."],
   ["Semana 2 - Dos lados", "Badge con verificación y apelación manual; llaves de API con cuota; landing dual en Hotmart."],
 ],
 "pricing": [
   ["Público", "gratis", "Verificador y reporte completo; motor del SEO"],
   ["Comercio verificado", "$9/mes", "Badge verificable, monitoreo continuo del dominio, sello en redes"],
   ["API Dev", "$15/mes", "1,000 veredictos/mes por API, webhooks, documentación en español"],
 ],
 "launch": ("Publicar el verificador en grupos de Facebook de compras y estafas locales (donde "
   "la gente ya pregunta 'esta página es confiable?') y en comunidades de desarrollo; cada "
   "dominio cuestionado genera tráfico y una página indexable. Ofrecer el badge gratis por tres "
   "meses a los primeros cincuenta comercios legítimos a cambio del sello visible que se "
   "convierte en prueba social pública del producto."),
 "precio_hotmart": "$9-15/mes", "esfuerzo": "3 días", "potencial": "Medio (con SEO alto)",
 "risk": ("Riesgo reputacional: un falso negativo que deje pasar un fraude. Mitigación: el "
   "veredicto siempre es probabilístico y explicable, con apelación humana, y la evidencia se "
   "muestra para que la decisión final sea del usuario."),
},
]
