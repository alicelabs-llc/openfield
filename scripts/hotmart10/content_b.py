# -*- coding: utf-8 -*-
"""Contenido del playbook - Productos 6 a 10 + Capítulo 12 (plan maestro). Sin emoji."""

PRODUCTS_B = [
{
 "num": 6, "key": "p06_citaya",
 "name": "CitaYa - Reservas por WhatsApp para negocios de servicio",
 "tagline": "La agenda que se llena sola mientras el barbero corta, el dentista atiende y la estilista trabaja",
 "cliente": "Barberías, salones de belleza, consultorios, estudios de tatuajes y spas de América Latina.",
 "pain": ("El negocio de citas pierde dinero en dos frentes diarios: la persona que querría agendar "
   "fuera de horario y no lo hace porque nadie contesta, y la ausencia silenciosa del cliente que "
   "reservó y no llegó, dejando el sillón vacío una hora completa. AgendaPro resolvió este "
   "mercado con 30,000 negocios y planes de 9 a 199 dólares, validando que el segmento paga; "
   "pero su flujo de reserva vive en su web propia y en su marketplace. El hueco: la reserva "
   "nativa dentro de WhatsApp (donde el cliente ya conversa), recordatorios que casi eliminan "
   "la ausencia, y anticipo opcional contra cancelaciones. El dueño ve el valor en números: un "
   "sillón vacío diario es mucho más que los 14 dólares del mes."),
 "market": ("AgendaPro demuestra precio y tamaño: plan individual de 9 dólares, básico de 29, "
   "premium de 59. CitaYa compite no contra el precio sino contra el canal: reservar desde el "
   "chat, sin instalar ni mandar al cliente a otra web. El plan de entrada de 14 dólares se "
   "vende solo contra el costo visible de las ausencias."),
 "competitors": [
   ["AgendaPro", "Mensual por profesionales", "$9-199/mes", "Líder LATAM; 30K negocios; web-propia de reservas"],
   ["SimplyBook.me / Booksy", "Mensual", "$15-60/mes", "Internacionales, en inglés o caros"],
   ["Agenda manual / cuaderno", "Tiempo del dueño", "$0 + ausencias", "El competidor real en el segmento bajo"],
 ],
 "estilo": ("La lección de AgendaPro a copiar es la prueba social masiva en el titular "
   "('+30.000 negocios crecen con AgendaPro') y el plan individual barato como puerta de entrada "
   "que luego escala. CitaYa copia la estructura de planes por número de profesionales y añade "
   "el diferencial visual de la página: la conversación real de WhatsApp donde el cliente "
   "reserva en tres mensajes. El copy hace aritmética visible: 'dos ausencias evitadas ya "
   "pagaron el mes'."),
 "copy": {
   "headline": "Tu agenda se llena sola por WhatsApp y las ausencias se acaban",
   "sub": ("CitaYa reserva, recuerda y reagenda dentro del chat que tus clientes ya usan. "
     "Recordatorios automáticos 24 y 1 hora antes, anticipo opcional contra no-shows, y tu "
     "agenda sincronizada con Google Calendar."),
   "bullets": [
     "El cliente reserva desde WhatsApp eligiendo servicio, profesional y horario",
     "Recordatorios automáticos que eliminan la mayoría de ausencias",
     "Anticipo o prepago opcional: quien cancela tarde, avisa o paga",
     "Google Calendar sincronizado en ambas direcciones",
     "Panel con comisiones por profesional y reportes del mes",
     "Configuración en 15 minutos con tus servicios reales",
   ],
   "para_quien": ("Para barberías, salones, consultorios y estudios con agenda propia. No es "
     "para clínicas con software médico certificado ni para cadenas con central de reservas."),
   "incluye": ["Agenda online con página propia de reservas", "Reserva y recordatorio por WhatsApp",
     "Hasta 5 profesionales según plan", "Sincronización Google Calendar", "Reportes de ocupación e ingresos",
     "Soporte en español por WhatsApp"],
   "garantia": ("Garantía de 7 días: si en la primera semana no se llena tu agenda con menos "
     "ausencias, devolución total."),
   "faq": [
     ["El cliente necesita descargar algo?", "No: reserva por WhatsApp o desde el link de tu agenda, sin instalar nada."],
     ["Que pasa si alguien no paga el anticipo?", "La cita queda en espera y se libera al rato; tu defines la política."],
     ["Puedo cobrar comisiones a mis barberos?", "Si, el panel calcula comisión por servicio y profesional automáticamente."],
   ],
   "cta": "Tu sillón vacío cuesta más que CitaYa. Pruébalo 7 días.",
 },
 "stack": ("FastAPI con modelo de disponibilidad por servicio-profesional-horario, motor de "
   "conflictos y zonas horarias; WhatsApp Cloud API para reserva y recordatorios con plantillas; "
   "OAuth de Google Calendar bidireccional; pagos de anticipo vía link (PayPhone/Mercado Pago); "
   "panel Next.js. Arquitectura compartida con WAOrder: mismo núcleo de WhatsApp, distinto "
   "dominio."),
 "fases": [
   ["Semana 1 - Motor de agenda", "Servicios, profesionales, disponibilidad, conflicto y página pública de reservas."],
   ["Semana 2 - WhatsApp y recordatorios", "Flujo de reserva por chat, plantillas de recordatorio, sincronización Google."],
   ["Semana 3 - Dinero y panel", "Anticipo opcional, comisiones, reportes, beta con 5 negocios del barrio."],
 ],
 "pricing": [
   ["Solo", "$14/mes", "1 profesional, agenda + WhatsApp + recordatorios"],
   ["Equipo", "$29/mes", "5 profesionales, comisiones, anticipo, reportes"],
   ["Anual", "$99/año", "Plan Solo congelado 12 meses"],
 ],
 "launch": ("Cinco negocios del entorno con tres meses gratis a cambio de usar el flujo real y "
   "dar testimonio con número de ausencias evitadas. Los grupos de 'barberías y salones' de "
   "Facebook y el marketplace de Instagram de la ciudad son el canal. El demo perfecto es el "
   "número del negocio del dueño: que el prospecto reserve una cita de prueba en su propio "
   "WhatsApp y vea la agenda bloquearse en vivo."),
 "precio_hotmart": "$14/mes", "esfuerzo": "3 semanas", "potencial": "Muy alto",
 "risk": ("Riesgo de mercado: AgendaPro baja su plan de entrada. Mitigación: la ventaja es de "
   "canal (WhatsApp nativo), no de precio; mantener velocidad de respuesta y foco en el "
   "segmento de 1-3 profesionales donde la plataforma grande es demasiado producto."),
},
{
 "num": 7, "key": "p07_reviewreply",
 "name": "ReviewReply - Respuestas con IA a reseñas de Google",
 "tagline": "Cada reseña de Google respondida como si el dueño tuviera todo el tiempo del mundo",
 "cliente": "Restaurantes, clínicas dentales, hoteles boutique y sucursales con Google Business Profile activo.",
 "pain": ("Responder reseñas mejora el posicionamiento local y la confianza, pero el dueño de un "
   "restaurante no va a redactar veinte respuestas al mes a medianoche. Las plataformas "
   "enterprise de reputación (Birdeye, Podium) cobran cientos de dólares mensuales y las "
   "herramientas nuevas de nicho (RepliFast y similares, entre 20 y 50 dólares) piden pegar y "
   "copiar manualmente. El hueco: un servicio completo en español que detecta la reseña, la "
   "responde con la voz del negocio, publica por sí mismo cuando es seguro y le pasa al dueño "
   "por WhatsApp solo las delicadas. La venta emocional es directa: la reseña de una estrella "
   "sin respuesta es la primera impresión de cientos de clientes futuros."),
 "market": ("Cada negocio con perfil de Google y reseñas activas es cliente potencial; el "
   "segmento medio (restaurantes y clínicas con 3-5 estrellas de promedio y flujo de reseñas "
   "semanal) paga 24 dólares mensuales sin discutir si el flujo funciona solo. Los multi-local "
   "(franquicias pequeñas, cadenas de clínicas) pagan por local."),
 "competitors": [
   ["Birdeye / Podium", "Enterprise", "$300+/mes", "Mucho más que responder; excesivo para pyme"],
   ["RepliFast y nicho", "Mensual", "$20-50/mes", "Copiar-pegar manual; sin publicación automática"],
   ["Respuestas a mano", "Tiempo del dueño", "$0 + descuido", "El estado real del 80% del mercado"],
 ],
 "estilo": ("Las herramientas de nicho venden con 'responde en segundos' y generador gratuito "
   "como imán (menuviel demuestra la táctica del generador gratis que engancha). ReviewReply "
   "copia el generador público gratuito como captación (tres respuestas gratis al día desde la "
   "web) y vende la automatización completa como producto: detección, redacción con voz de "
   "marca, publicación automática de las positivas y aprobación por WhatsApp de las críticas. "
   "La página muestra el antes/después: la reseña de una estrella y la respuesta profesional "
   "generada."),
 "copy": {
   "headline": "Todas tus reseñas de Google respondidas bien, incluso las malas",
   "sub": ("ReviewReply detecta cada reseña nueva, escribe la respuesta con el tono de tu "
     "negocio y la publica sola. Las críticas llegan a tu WhatsApp con la respuesta propuesta "
     "para tu aprobación en un clic. Tu reputación local, en piloto automático."),
   "bullets": [
     "Responde sola las reseñas positivas y neutrales en minutos",
     "Las críticas te llegan por WhatsApp con la respuesta lista para aprobar",
     "Tono personalizado por negocio: formal, cercano o con humor",
     "Escalamiento de casos sensibles con plantillas de manejo de crisis",
     "Reporte mensual: nota media, velocidad de respuesta y evolución",
     "Multi-local: cadenas pequeñas con panel por sucursal",
   ],
   "para_quien": ("Para negocios con Google Business Profile activo y reseñas semanales que hoy "
     "no responden o responden tarde. No es para gestores de reputación de grandes marcas."),
   "incluye": ["Conexión a Google Business Profile", "Generación IA con voz de marca",
     "Publicación automática de positivas", "Aprobación por WhatsApp de críticas",
     "Reporte mensual de reputación", "Hasta 1 local (planes multi-local disponibles)"],
   "garantia": ("Garantía de 7 días: si tus reseñas no se responden mejor que lo que haces hoy "
     "(nada), devolución total."),
   "faq": [
     ["Puede publicar respuestas sin que yo las vea?", "Solo las positivas y neutrales dentro de tu tono aprobado; toda reseña menor a 3 estrellas pide tu visto bueno por WhatsApp."],
     ["Aprende de mi negocio?", "Si: le das 3 respuestas de ejemplo y un parrafo de tu estilo, y el tono se ajusta a la voz del local."],
     ["Que pasa con Google si cambio de opinión?", "Se desconecta con un clic y no queda rastro de automatización."],
   ],
   "cta": "Tu próxima reseña de 1 estrella merece respuesta profesional. Actívalo hoy.",
 },
 "stack": ("Worker de sondeo de la API de Google Business Profile (con OAuth por local), "
   "generación con LLM económico con contexto de marca y reglas de escalamiento, cola de "
   "aprobaciones con botón de publicación, panel Next.js multi-local, reportes mensuales "
   "automáticos por email. Nota clave: la API GBP exige verificación del negocio; el flujo de "
   "onboarding guía el permiso de administrador."),
 "fases": [
   ["Semana 1 - Detección y generación", "OAuth GBP, sondeo de reseñas nuevas, generador con tono configurable."],
   ["Semana 2 - Automatización completa", "Publicación de positivas, aprobación por WhatsApp de críticas, reglas de escalamiento."],
 ],
 "pricing": [
   ["Local", "$24/mes", "1 local, todo automatizado"],
   ["Cadena", "$59/mes", "Hasta 5 locales, panel consolidado, usuarios extra"],
   ["Anual", "$179/año", "Plan Local congelado 12 meses"],
 ],
 "launch": ("El generador público gratis (3 respuestas al día) se lanza en grupos de "
   "restaurantes y clínicas para captar correos; cada usuario del generador recibe la oferta de "
   "automatización completa por menos de lo que cuesta una pizza familiar. Demostración en "
   "frío: buscar cinco restaurantes locales con reseñas de una estrella sin responder, redactar "
   "las respuestas con la herramienta y enviárselas al dueño con el reporte adjunto."),
 "precio_hotmart": "$24/mes", "esfuerzo": "2 semanas", "potencial": "Alto",
 "risk": ("Riesgo de dependencia de la API de Google Business Profile y sus límites. Mitigación: "
   "respetar cuotas oficiales, cachear y ofrecer degradación elegante (borrador por email si la "
   "publicación automática no está disponible para el local)."),
},
{
 "num": 8, "key": "p08_postfactory",
 "name": "PostFactory - Contenido con IA para redes de negocios locales",
 "tagline": "El mes completo de publicaciones de tu negocio, creado y programado mientras atiendes",
 "cliente": "Tiendas, talleres, veterinarias, gimnasios de barrio y negocios de servicio con Instagram/Facebook activos pero descuidados.",
 "pain": ("El negocio local sabe que tiene que publicar en redes, pero entre atender y operar la "
   "pauta se muere: publica tres veces al mes, sin consistencia y sin estrategia. Las "
   "herramientas globales (Predis.ai desde 29 dólares, ContentStudio 19-49) generan contenido "
   "genérico en inglés que suena a plantilla y exigen que el dueño aprenda otra plataforma. El "
   "hueco: contenido con sabor local (el barrio, la promoción del mes, la fecha del sector), "
   "imágenes con la identidad del negocio, aprobación por WhatsApp del dueño (otra vez el canal "
   "ganador) y autopublicación real vía Meta API. El dueño solo aprueba: todo lo demás se hace "
   "solo."),
 "market": ("Es el mismo comprador de CitaYa y MenuQR (el negocio de barrio digitalizando su "
   "operación) con un dolor más visible porque la inactividad en redes es pública. El bundle "
   "natural con los otros productos del portafolio convierte a este producto en el upsell más "
   "barato de la casa."),
 "competitors": [
   ["Predis.ai", "Mensual", "desde $29/mes", "Genera y programa; genérico; inglés"],
   ["ContentStudio / Buffer IA", "Mensual", "$19-49/mes", "Calendarios potentes; curva alta"],
   ["Community manager freelance", "Mensual", "$150-400/mes", "El competidor real: caro o inexistente en el segmento"],
 ],
 "estilo": ("Predis vende 'de la idea al post publicado' con ejemplos visuales de primeros "
   "planos. PostFactory copia la demostración visual (rejilla de Instagram con los posts "
   "generados) pero ancla el diferencial en dos capturas: la conversación de WhatsApp donde el "
   "dueño aprueba la pauta de la semana y el calendario con colores por tipo de post. El copy "
   "compara directamente contra el community manager: 'todo lo que hace tu community manager "
   "por 200 dólares, sin descansos'."),
 "copy": {
   "headline": "Tu Instagram lleno todo el mes, aprobado desde tu WhatsApp",
   "sub": ("PostFactory crea tus posts con fotos y promociones reales de tu negocio, arma el "
     "calendario de la semana y publica solo. Tú solo abres el chat, ves la pauta y dices "
     "aprobado."),
   "bullets": [
     "12 a 20 posts al mes con tus fotos, promos y fechas del barrio",
     "Copys con hashtags locales y llamadas a la acción reales",
     "Imágenes con plantillas de tu marca (colores y logo)",
     "Aprobación en un mensaje de WhatsApp: aprueba, edita o descarta",
     "Autopublicación en Instagram y Facebook vía API oficial",
     "Reporte simple de alcance y mejores horarios, sin jerga",
   ],
   "para_quien": ("Para negocios con fotos propias y algo que contar que hoy publican poco o "
     "nada. No es para marcas con agencia creativa ni para quien exige diseño editorial."),
   "incluye": ["Generación semanal de pauta", "Plantillas de imagen con tu marca",
     "Calendario editorial aprobable por WhatsApp", "Autopublicación Meta (IG + FB)",
     "Reporte mensual simple", "Guía de qué fotos tomar con el celular"],
   "garantia": ("Garantía de 7 días: si la primera semana de posts no te parece mejor de lo que "
     "publicas hoy, devolución total."),
   "faq": [
     ["Usa mis fotos reales?", "Si, la guia te ensena que capturar con el celular en 10 minutos y el sistema las mezcla con plantillas de tu marca."],
     ["Puede sonar robotico?", "El tono se entrena con tus posts anteriores y tu manera de escribir; ademas tu apruebas todo antes de publicar."],
     ["Funciona para TikTok?", "Al lanzar publica IG y Facebook; los guiones para Reels/TikTok estan en el roadmap inmediato."],
   ],
   "cta": "Deja de publicar a la desesperada. Tu pauta de la semana llega cada lunes.",
 },
 "stack": ("FastAPI con generación de copys por LLM con contexto del negocio (catálogo, "
   "promos, tono), imágenes vía plantillas dinámicas (Canvas API propia o generación con "
   "modelos de imagen cuando conviene), Meta Graph API para publicación programada, flujo de "
   "aprobación por WhatsApp Cloud API (reutilizado de WAOrder/CitaYa), panel de calendario "
   "Next.js."),
 "fases": [
   ["Semanas 1-2 - Generación", "Onboarding del negocio, brief inicial, generación de copys + imágenes con plantilla, vista previa."],
   ["Semanas 3-4 - Ciclo completo", "Aprobación por WhatsApp, autopublicación Meta, calendario, reporte mensual, beta con 8 negocios."],
 ],
 "pricing": [
   ["Barrio", "$17/mes", "12 posts/mes, IG + FB, aprobación por WhatsApp"],
   ["Activo", "$29/mes", "20 posts/mes, stories, reporte de horarios"],
   ["Anual", "$129/año", "Plan Barrio congelado 12 meses"],
 ],
 "launch": ("Ocho negocios del entorno con un mes gratis a cambio de publicar lo que genere el "
   "sistema; sus perfiles reales son la galería de la landing. El generador gratuito de 'un post "
   "al día' para nuevos negocios funciona como captación en grupos de emprendedores. El bundle "
   "con CitaYa ('tu negocio agenda y publica solo') es la oferta de venta cruzada natural."),
 "precio_hotmart": "$17/mes", "esfuerzo": "3-4 semanas", "potencial": "Medio-alto",
 "risk": ("Riesgo de calidad creativa: el contenido genérico mata la retención. Mitigación: el "
   "tono entrenado por negocio, las fotos reales obligatorias en el onboarding y la aprobación "
   "humana de cada post."),
},
{
 "num": 9, "key": "p09_menuqr",
 "name": "MenuQR - Carta digital QR con pedidos a WhatsApp",
 "tagline": "El comensal escanea, pide desde la mesa y el pedido cae en tu WhatsApp",
 "cliente": "Restaurantes, cafeterías, bares y food trucks de América Latina que quieren carta digital y pedidos organizados.",
 "pain": ("La carta impresa cuesta entre 150 y 400 dólares por tirada y envejece al primer cambio "
   "de precio; el QR gratuito básico (BuenaCarta, SitioYa) solo muestra un PDF que nadie disfruta "
   "leer; las plataformas completas de pedidos cobran comisión por venta o mensualidades "
   "empresariales. Treggio demostró el hueco exacto: 'QR + pedidos directos a WhatsApp, sin "
   "comisiones, listo en 3 minutos'. El comprador entiende el valor sin educación previa: la "
   "carta se actualiza sola, el pedido llega escrito y estructurado (nada de pedir de memoria al "
   "mesero de WhatsApp), y la mesa ordena sin esperar."),
 "market": ("Cada restaurante que sobrevivió la pandemia tiene un QR viejo apuntando a un PDF "
   "congelado. La conversión de ese instalador base es rápida porque el dueño ya entiende el "
   "concepto; la venta se gana por la demo: actualizar un precio y verlo vivo en la carta en "
   "segundos."),
 "competitors": [
   ["Treggio", "Freemium + planes", "gratis - ~$20/mes", "Competidor conceptual directo; validar su copy"],
   ["BuenaCarta / SitioYa", "Gratis con límites", "$0", "PDF/imagen estática; sin pedidos"],
   ["FineDine y similares", "Mensual", "$30+/mes", "Internacionales, en inglés, caros"],
 ],
 "estilo": ("La táctica ganadora del segmento (Treggio) es el triángulo 'sin comisiones + listo "
   "en minutos + pedidos a tu WhatsApp' y el generador gratuito como puerta. MenuQR copia ese "
   "triángulo literalmente en el copy y lo apoya con el detalle que las cartas gratuitas no "
   "tienen: estados del pedido, estadísticas de platos y propina digital opcional. La landing "
   "muestra el QR real escaneable de demo: el prospecto prueba el flujo completo desde su "
   "celular sin hablar con nadie."),
 "copy": {
   "headline": "Carta QR que se actualiza sola y pedidos que llegan listos a tu WhatsApp",
   "sub": ("MenuQR convierte tu carta en una experiencia con fotos y alérgenos, actualiza "
     "precios al instante y recibe los pedidos estructurados de cada mesa directamente en tu "
     "WhatsApp. Sin comisiones por venta, sin apps para el comensal."),
   "bullets": [
     "Carta web con fotos, descripciones y alérgenos, siempre al día",
     "QR por mesa listo para imprimir en 3 minutos",
     "El comensal arma su pedido y te llega estructurado a WhatsApp",
     "Estados del pedido: cocina, en preparación, entregado",
     "Estadísticas de platos más vendidos y horas pico",
     "Sin comisión por venta: pagas una cuota plana",
   ],
   "para_quien": ("Para restaurantes, cafeterías y food trucks que hoy tienen un QR viejo o una "
     "carta que hay que reimprimir. No es para cadenas con sistema POS integrado."),
   "incluye": ["Carta digital ilimitada con fotos", "QRs por mesa listos para imprimir",
     "Pedidos a WhatsApp estructurados", "Panel de edición al instante",
     "Estados y estadísticas de venta", "Soporte en español"],
   "garantia": ("Garantía de 7 días: monta tu carta real; si en una semana el flujo no te "
     "convence, devolución total."),
   "faq": [
     ["El comensal necesita app?", "No: escanea el QR y abre la carta en su navegador."],
     ["Y si el pedido llega incompleto?", "El pedido sale con mesa, platos, notas y propina; si falta algo el mesero lo completa en 5 segundos."],
     ["Puedo tener varios menus (dia/noche)?", "Si: menus por horario con activacion automatica."],
   ],
   "cta": "Tu carta vieja esta costandote ventas. Monta la nueva en 3 minutos.",
 },
 "stack": ("Aplicación web SSR (Next.js o FastAPI + Jinja) con carta por restaurante, editor "
   "en línea con guardado instantáneo, generador de QR por mesa con enlace profundo que arma "
   "el mensaje de WhatsApp (wa.me con texto estructurado) en fase 1 y pasaje a Cloud API con "
   "estados en fase 2; PostgreSQL simple; panel con estadísticas agregadas."),
 "fases": [
   ["Semana 1 - Carta y QR", "Editor instantáneo, carta móvil bonita, QR por mesa, pedido a WhatsApp por enlace."],
   ["Semana 2 - Producto completo", "Estados del pedido, estadísticas, demo pública escaneable, landing con la demo."],
 ],
 "pricing": [
   ["Mesita", "$11/mes", "1 local, carta ilimitada, QRs, pedidos WhatsApp"],
   ["Cocina", "$19/mes", "+ estados del pedido y estadísticas"],
   ["Anual", "$79/año", "Plan Mesita congelado 12 meses"],
 ],
 "launch": ("Montar la carta real de tres restaurantes del entorno gratis por tres meses a "
   "cambio del sello 'pedidos por MenuQR' en sus mesas y redes; el QR de demo escaneable en la "
   "landing cierra ventas sin reunión. Grupos de 'gastronomía y emprendimiento' locales y el "
   "contacto directo por Instagram a cafeterías nuevas (abrieron = necesitan carta) son el "
   "canal de entrada."),
 "precio_hotmart": "$11/mes", "esfuerzo": "2 semanas", "potencial": "Alto",
 "risk": ("Riesgo de mercadeo: el competidor gratuito. Mitigación: el valor está en pedidos "
   "estructurados y estadísticas, no en la carta; el plan gratuito propio (carta sin pedidos) "
   "alimenta el embudo."),
},
{
 "num": 10, "key": "p10_licitalert",
 "name": "LicitAlert - Alertas inteligentes de licitaciones SERCOP",
 "tagline": "El proceso público perfecto para tu empresa llega a tu Telegram antes de que lo lea tu competencia",
 "cliente": "Proveedores del Estado ecuatoriano: distribuidoras, consultoras, constructoras pequeñas y pymes B2B que viven de compra pública.",
 "pain": ("El portal público de compra pública publica cada día cientos de procesos; el proveedor "
   "que no revisa a diario pierde procesos por vencimiento de plazos o ni se entera de rubros "
   "que calzan perfecto con su catálogo. Las notificaciones oficiales son genéricas (todo lo "
   "publicado) y los consultores de vigilancia de mercado son caros y manuales. El hueco: "
   "clasificación semántica real (rubros NPU interpretados, montos, cantones y fechas filtradas "
   "contra el perfil del proveedor) con alerta instantánea por Telegram y email, más un "
   "dashboard de oportunidades con plazos. En Colombia la equivalencia ya existe (portales de "
   "vigilancia de SECOP con suscripciones), lo que valida el modelo; en Ecuador el espacio "
   "está abierto."),
 "market": ("Es el producto B2B más específico del portafolio y el de mayor valor percibido por "
   "usuario: un solo contrato ganado paga años de suscripción. La base de proveedores "
   "registrados ante el SERCOP se cuenta en decenas de miles; el plan de 29 dólares mensuales "
   "es una decisión operativa, no emocional."),
 "competitors": [
   ["Notificaciones del portal oficial", "Gratuito", "$0", "Genéricas, sin filtro por perfil, sin prioridad"],
   ["Consultores de vigilancia", "Retainer", "$200+/mes", "Manuales, lentos, caros para pyme"],
   ["Hojas de cálculo internas", "Tiempo del equipo", "$0 + horas", "El estado real del proveedor medio"],
 ],
 "estilo": ("Los portales de vigilancia colombianos venden con 'no pierdas más procesos por "
   "enterarte tarde' y capturas del email de alerta. LicitAlert copia esa estructura y añade "
   "el diferencial visual: la alerta de Telegram real con el proceso resumido (objeto, monto, "
   "cierre, match con tu rubro) y el contador de 'procesos que calzaron con tu perfil esta "
   "semana'. El copy es de dinero perdido: 'el contrato que no sabías que existía'."),
 "copy": {
   "headline": "Cada licitación que calza con tu empresa, en tu Telegram el mismo día",
   "sub": ("LicitAlert lee todos los procesos de compra pública, entiende qué rubros son tuyos "
     "y te avisa al instante con objeto, monto y fecha de cierre. Deja de revisar el portal a "
     "mano: tu próxima adjudicación no se te escapa por enterarte tarde."),
   "bullets": [
     "Alertas instantáneas por Telegram y email al publicarse el proceso",
     "Clasificación semántica por rubros NPU contra el perfil de tu empresa",
     "Filtros por monto, cantón y fecha de cierre",
     "Dashboard de oportunidades con plazos y estados de seguimiento",
     "Histórico de procesos vistos, presentados y adjudicados",
     "Reporte semanal del mercado en tu categoría",
   ],
   "para_quien": ("Para proveedores del Estado que ya están habilitados y quieren dejar de "
     "depender de la suerte y de revisar el portal a mano. No es asesoría legal ni garantiza "
     "adjudicaciones: garantiza enterarte a tiempo."),
   "incluye": ["Perfil de empresa con rubros NPU", "Alertas Telegram + email en tiempo real",
     "Dashboard de oportunidades y plazos", "Filtros por monto y cantón",
     "Reporte semanal de tu categoría", "Soporte en español"],
   "garantia": ("Garantía de 7 días: si en tu primera semana no llega ni un proceso que calce "
     "con tu perfil, devolución total."),
   "faq": [
     ["Es oficial? Usa datos validos?", "Usa exclusivamente los datos publicos del portal oficial de compra publica; no altera plazos ni contenidos."],
     ["Como sabe que rubros son mios?", "En el onboarding registras tus rubros NPU y palabras clave; el clasificador aprende y tu ajustas con un clic."],
     ["Sirve para otros paises?", "Al lanzar, Ecuador (SERCOP); Colombia (SECOP) en el roadmap inmediato."],
   ],
   "cta": "El proceso perfecto para ti se publica hoy. Enterate antes que tu competencia.",
 },
 "stack": ("Crawler diario del portal público y datasets abiertos (respetando términos y "
   "frecuencias), normalización de procesos, clasificador semántico de rubros NPU + matching "
   "IA contra perfiles, colas de notificación Telegram/email, PostgreSQL con pipeline de "
   "deduplicación, dashboard Next.js con pipeline de oportunidades y reportes semanales."),
 "fases": [
   ["Semana 1 - Fuente y clasificación", "Crawler estable del portal, normalización, clasificador NPU básico con ajuste manual."],
   ["Semana 2 - Alertas y producto", "Telegram/email, perfiles de empresa, dashboard, beta con 5 proveedores reales."],
 ],
 "pricing": [
   ["Proveedor", "$29/mes", "1 perfil de empresa, alertas ilimitadas, dashboard"],
   ["Multi-rubro", "$49/mes", "3 perfiles/rubros, reportes avanzados, historial extendido"],
   ["Anual", "$199/año", "Plan Proveedor congelado 12 meses"],
 ],
 "launch": ("Cinco proveedores reales del entorno con dos meses gratis a cambio de calibrar "
   "sus perfiles y dar testimonio del primer proceso encontrado. La demo perfecta es en vivo: "
   "con el perfil del prospecto configurado, mostrar los procesos de esa semana que calzaron y "
   "que él no conocía. El reporte semanal gratuito de los procesos publicados en una categoría "
   "popular (por ejemplo, equipos de cómputo) funciona como lead magnet en grupos de "
   "proveedores."),
 "precio_hotmart": "$29/mes", "esfuerzo": "2 semanas", "potencial": "Nicho sólido",
 "risk": ("Riesgo de fuente: cambios en el portal oficial. Mitigación: dos rutas de datos "
   "(portal y datasets abiertos) y alerta interna si el flujo de procesos cae a cero."),
},
]

CH12 = {
 "intro": ("Diez productos no se lanzan a la vez: se lanzan en oleadas donde cada producto "
   "financia y alimenta al siguiente. Este capítulo ordena la ejecución en un plan de cuatro "
   "meses, define las sinergias técnicas que abaratan cada producto nuevo y describe el embudo "
   "de Hotmart que convierte tráfico en suscripciones."),
 "fases": [
   ["Oleada 0 - Semana 1: la maquinaria", ("Empaquetar ScamGuard (el prototipo ya existe) y publicarlo en Hotmart con la "
     "estructura completa de landing, precios y garantía. El objetivo no es su ingreso sino "
     "montar la maquinaria completa de venta: cuenta Hotmart, producto, página de ventas, "
     "webhook de entrega, soporte. Todo error de maquinaria se comete aquí, donde el producto "
     "es gratis y el riesgo es cero.")],
   ["Oleada 1 - Semanas 2-4: el producto bandera", ("Construir y lanzar WAOrder, el producto de mayor mercado y el que mejor "
     "demuestra el estilo del portafolio. En paralelo, MenuQR (dos semanas) comparte el mismo "
     "embudo de negocio local: los restaurantes que compran carta digital son prospectos del "
     "bot de pedidos y viceversa. Meta de la oleada: 20 clientes de pago combinados.")],
   ["Oleada 2 - Mes 2: verticales de servicio", ("CitaYa y ReviewReply apuntan al mismo comprador (negocio de servicio con "
     "agenda y reputación) y reutilizan el núcleo de WhatsApp ya construido. El bundle de dos "
     "productos para el mismo cliente es la primera prueba del efecto portafolio. Meta: 30 "
     "clientes combinados y las primeras suscripciones anuales.")],
   ["Oleada 3 - Mes 3: captadores B2B", ("LeadMiner y PriceRadar apuntan a compradores profesionales (agencias y "
     "sellers) con tickets mayores y renovación estable. Ambos se apoyan en demos con datos "
     "reales del prospecto, la táctica de conversión más fuerte del portafolio. Meta: 25 "
     "clientes combinados con ticket promedio superior a la oleada anterior.")],
   ["Oleada 4 - Mes 4+: los exigentes", ("PostFactory, LicitAlert y FacturaEC cierran el portafolio: requieren más "
     "semanas de construcción o adaptación regulatoria. Llegan a un mercado ya cálido con "
     "testimonios de las oleadas previas. FacturaEC en particular entra con beta cerrada de dos "
     "semanas antes de vender.")],
 ],
 "sinergias": ("Todo el portafolio comparte un esqueleto técnico único: FastAPI con PostgreSQL, "
   "panel web Next.js, núcleo de WhatsApp Cloud API con aprobaciones por chat (reutilizado en "
   "WAOrder, CitaYa, ReviewReply, PostFactory y MenuQR), colas de tareas, y el módulo de "
   "facturación Hotmart con webhooks de suscripción escrito una sola vez. La segunda copia de "
   "cualquier producto cuesta cerca de la mitad de la primera y la cuarta se comporta como "
   "montaje, no como desarrollo. La regla operativa es no duplicar: cada pieza nueva (motor de "
   "agenda, clasificador NPU, generador de copys) nace como módulo reutilizable del esqueleto."),
 "funnel": ("El embudo de Hotmart se apoya en tres piezas. Primera: el magnetto gratuito por "
   "producto (el verificador público de ScamGuard, las tres respuestas gratis de ReviewReply, "
   "el reporte semanal de LicitAlert, la mini-lista de diez leads de LeadMiner) que convierte "
   "curiosos en contactos. Segunda: la página de ventas construida con el copy de cada "
   "capítulo, garantía visible y demo jugable donde exista (el QR escaneable de MenuQR, el "
   "bot real de WAOrder). Tercera: el programa de afiliados de Hotmart activado con comisión "
   "del 40 por ciento en el primer mes: cientos de afiliados hispanohablantes venden el "
   "portafolio sin costo fijo, y el producto con mejor conversión absorbe el tráfico."),
 "proyeccion": ("Proyección conservadora a doce meses con ejecución disciplinada: cinco productos "
   "activos con treinta clientes de promedio a 20 dólares mensuales equivalen a unos 3,000 "
   "dólares de ingreso recurrente mensual, antes de la comisión de plataforma (aproximadamente "
   "10 por ciento entre comisión Hotmart y costos de pasarela) y costos de infraestructura "
   "(del orden de 50 a 100 dólares mensuales para servir todo el portafolio en la nube). El "
   "resultado neto esperable del primer año completo se ubica entre 20,000 y 35,000 dólares, "
   "con la característica más valiosa: el ingreso es recurrente y cada producto nuevo del "
   "esqueleto cuesta menos que el anterior."),
 "checklist": [
   "Cuenta Hotmart verificada con datos de la LLC y cuenta bancaria conectada",
   "Producto creado con pago único o suscripción, precio de lanzamiento y cupón fundador",
   "Página de ventas con el copy del capítulo, demo o video de 90 segundos y garantía visible",
   "Webhook de Hotmart conectado al sistema de entrega (licencia + acceso al panel)",
   "Emails de bienvenida y de falla de pago configurados",
   "Programa de afiliados abierto al 40 por ciento el primer mes",
   "Soporte por WhatsApp definido y horario publicado",
   "Métricas semanales: visitas, conversión, churn y ticket promedio",
 ],
}
