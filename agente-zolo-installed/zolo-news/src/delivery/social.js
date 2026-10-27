// ============================================================
// ZOLO NEWS — Canal SOCIAL (Facebook / Instagram / TikTok)
// Subagente 125-C · AliceLabs
//
// SIN tokens NO se llama a ninguna API: cada canal devuelve
//   {channel, status:'necesita_configuracion', note:<instrucción concreta>}
// o {channel, status:'deshabilitado'} si enabled !== true.
//
// Las funciones de publicación quedan LISTAS (con try/catch y el comentario
// exacto de dónde iría la llamada) pero SIN subida real, porque requieren
// app review / tokens aprobados. Paso a paso completo: docs/CANALES.md.
// ============================================================

const MB = 1024 * 1024;

/**
 * Orquesta los 3 canales sociales según cfg.channels.
 * @param {object} channels - cfg.channels (facebook, instagram, tiktok)
 * @param {{sections?:Array, reportMd?:string, videoPath?:string|null, fecha?:string}} contexto
 * @returns {Promise<Array<{channel:string, status:string, note?:string}>>}
 */
export async function deliverSocial(channels = {}, contexto = {}) {
  void contexto; // se usará cuando haya tokens (texto del post / video)
  const salida = [];
  for (const nombre of ['facebook', 'instagram', 'tiktok']) {
    const canal = channels?.[nombre];
    if (!canal || canal.enabled !== true) {
      salida.push({
        channel: nombre,
        status: 'deshabilitado',
        note: canal?.note || 'poner enabled:true y credenciales en config.json — ver docs/CANALES.md',
      });
      continue;
    }
    try {
      const r = await publicar(nombre, canal, contexto);
      salida.push(r);
    } catch (e) {
      salida.push({ channel: nombre, status: 'error', note: `${e?.message || e}` });
    }
  }
  return salida;
}

async function publicar(nombre, canal, contexto) {
  switch (nombre) {
    case 'facebook': return publicarFacebook(canal, contexto);
    case 'instagram': return publicarInstagram(canal, contexto);
    case 'tiktok': return publicarTikTok(canal, contexto);
    default: return { channel: nombre, status: 'deshabilitado', note: 'canal social desconocido' };
  }
}

// ------------------------------------------------------------------
// FACEBOOK — Meta Graph API · /{page-id}/feed (texto) o /photos (imagen)
// ------------------------------------------------------------------
async function publicarFacebook(canal, contexto) {
  // FUTURO (cuando exista canal.pageToken + canal.pageId con permiso pages_manage_posts):
  //
  //   const mensaje = construirPostSocial(contexto); // 3 titulares + clima + curiosidad
  //   const res = await fetch(`https://graph.facebook.com/v21.0/${canal.pageId}/feed`, {
  //     method: 'POST',
  //     body: new URLSearchParams({ message: mensaje, access_token: canal.pageToken }),
  //   });
  //   const data = await res.json();
  //   if (!res.ok || data.error) throw new Error(data.error?.message || `HTTP ${res.status}`);
  //   return { channel:'facebook', status:'publicado', note:`post ${data.id}` };
  //
  if (!canal.pageToken || !canal.pageId) {
    return {
      channel: 'facebook',
      status: 'necesita_configuracion',
      note: 'Faltan facebook.pageToken (Page Access Token con permisos pages_manage_posts) y facebook.pageId — paso a paso en docs/CANALES.md',
    };
  }
  return {
    channel: 'facebook',
    status: 'pendiente_implementacion',
    note: 'Token presente: falta activar la llamada a Graph API /feed marcada con FUTURO en src/delivery/social.js (tras app review de Meta)',
  };
}

// ------------------------------------------------------------------
// INSTAGRAM — Instagram Graph API (publicación en 2 pasos: contenedor → publish)
// ------------------------------------------------------------------
async function publicarInstagram(canal, contexto) {
  // FUTURO (cuando exista canal.igUserId + canal.igToken con permiso instagram_content_publish):
  //
  //   const caption = construirPostSocial(contexto);
  //   // Paso 1: crear contenedor (requiere image_url público o video_url accesible)
  //   const r1 = await fetch(`https://graph.facebook.com/v21.0/${canal.igUserId}/media`, {
  //     method: 'POST',
  //     body: new URLSearchParams({ image_url: canal.imageUrl || '', caption, access_token: canal.igToken }),
  //   });
  //   const c1 = await r1.json();
  //   // Paso 2: publicar el contenedor
  //   const r2 = await fetch(`https://graph.facebook.com/v21.0/${canal.igUserId}/media_publish`, {
  //     method: 'POST',
  //     body: new URLSearchParams({ creation_id: c1.id, access_token: canal.igToken }),
  //   });
  //
  if (!canal.igToken || !canal.igUserId) {
    return {
      channel: 'instagram',
      status: 'necesita_configuracion',
      note: 'Faltan instagram.igUserId (ID de cuenta profesional) e instagram.igToken (con permiso instagram_content_publish) — paso a paso en docs/CANALES.md',
    };
  }
  return {
    channel: 'instagram',
    status: 'pendiente_implementacion',
    note: 'Token presente: falta activar la publicación en 2 pasos (media → media_publish) marcada con FUTURO en src/delivery/social.js',
  };
}

// ------------------------------------------------------------------
// TIKTOK — Content Posting API (upload de video bulletin.mp4)
// ------------------------------------------------------------------
async function publicarTikTok(canal, contexto) {
  // FUTURO (cuando exista canal.accessToken de una app aprobada con video.publish):
  //
  //   // 1) Solicitar URL de upload: POST https://open.tiktokapis.com/v2/post/publish/video/init/
  //   //    body: { post_info:{ title, privacy_level:"SELF_ONLY" }, source_info:{ source:"FILE_UPLOAD", video_size, chunk_size, total_chunk_count:1 } }
  //   // 2) PUT del archivo (bulletin.mp4 ≤ 64 MB... normalmente el boletín pesa menos)
  //   const size = fs.statSync(contexto.videoPath).size;
  //   if (size > 64 * MB) throw new Error('video demasiado grande para TikTok');
  //
  if (!canal.accessToken) {
    return {
      channel: 'tiktok',
      status: 'necesita_configuracion',
      note: 'Falta tiktok.accessToken (app aprobada en developers.tiktok.com con Content Posting API y permiso video.publish) — paso a paso en docs/CANALES.md',
    };
  }
  return {
    channel: 'tiktok',
    status: 'pendiente_implementacion',
    note: 'Token presente: falta activar el flujo video/init/ + PUT marcado con FUTURO en src/delivery/social.js (requiere app aprobada por TikTok)',
  };
}

/** Post social de texto: 3 titulares + clima + curiosidad (reutilizable cuando haya tokens). */
export function construirPostSocial({ sections = [], fecha = '' } = {}) {
  const noticias = sections.filter((s) => s.kind === 'news').slice(0, 3);
  const clima = sections.find((s) => s.kind === 'weather');
  const curiosa = sections.find((s) => s.kind === 'curious');
  const lineas = [`📰 ZOLO Noticias${fecha ? ` — ${fecha}` : ''}`, ''];
  for (const n of noticias) {
    lineas.push(`• ${n.title}${n.source ? ` (${n.source})` : ''}`);
    if (n.url) lineas.push(`  ${n.url}`);
  }
  if (clima?.text) lineas.push('', `🌤️ ${String(clima.text).slice(0, 160)}`);
  if (curiosa?.text) lineas.push('', `🎲 ${String(curiosa.text).slice(0, 160)}`);
  lineas.push('', '— ZOLO · AliceLabs');
  return lineas.join('\n').slice(0, 2000);
}

export default deliverSocial;
