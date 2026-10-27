// ============================================================
// ZOLO NEWS — Pipeline de medios (implementación del Subagente 125-B)
// Re-exporta EXACTAMENTE el contrato que consume el núcleo (125-A):
//   makeAvatar(cfg)                                  → {path, cached}
//   makeAudio(sections, cfg)                         → [{index, path, seconds}]
//   makeNewsImages(sections, cfg)                    → [{index, path}]
//   makeVideo({sections, audio, avatar, images}, cfg) → {videoPath} | {videoPath:null, reason}
// ============================================================

export { makeAvatar } from './avatar.js';
export { makeAudio } from './tts.js';
export { makeNewsImages } from './images.js';
export { makeVideo } from './video.js';
