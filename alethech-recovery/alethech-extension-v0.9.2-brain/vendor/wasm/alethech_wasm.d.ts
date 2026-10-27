/* tslint:disable */
/* eslint-disable */

/**
 * Generate a fresh 32-byte recovery secret, return as base64url string.
 * Used by the UI when the user wants to create a new recovery code.
 */
export function generate_recovery_secret(): string;

export function open_aleth_payload(blob: Uint8Array, passphrase: string): Uint8Array;

export function open_aleth_v1(blob: Uint8Array, passphrase: string): Uint8Array;

export function open_aleth_v2_passphrase(blob: Uint8Array, passphrase: string): Uint8Array;

export function open_aleth_v2_recovery(blob: Uint8Array, recovery_code: string): Uint8Array;

export function recover_aleth_v2(blob: Uint8Array, recovery_code: string, new_passphrase: string, rotate_recovery: boolean): string;

export function reseal_aleth_v2(plaintext: Uint8Array, passphrase: string, recovery_secret_b64: string, container_id_b64: string): string;

export function rewrite_aleth_payload(blob: Uint8Array, current_passphrase: string, plaintext: Uint8Array, new_passphrase: string, recovery_secret_b64: string): string;

export function seal_aleth_payload(plaintext: Uint8Array, passphrase: string): Uint8Array;

export function seal_aleth_v2(plaintext: Uint8Array, passphrase: string, recovery_secret_b64: string): string;

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
    readonly memory: WebAssembly.Memory;
    readonly generate_recovery_secret: () => [number, number, number, number];
    readonly open_aleth_payload: (a: number, b: number, c: number, d: number) => [number, number, number, number];
    readonly open_aleth_v1: (a: number, b: number, c: number, d: number) => [number, number, number, number];
    readonly open_aleth_v2_passphrase: (a: number, b: number, c: number, d: number) => [number, number, number, number];
    readonly open_aleth_v2_recovery: (a: number, b: number, c: number, d: number) => [number, number, number, number];
    readonly recover_aleth_v2: (a: number, b: number, c: number, d: number, e: number, f: number, g: number) => [number, number, number, number];
    readonly reseal_aleth_v2: (a: number, b: number, c: number, d: number, e: number, f: number, g: number, h: number) => [number, number, number, number];
    readonly rewrite_aleth_payload: (a: number, b: number, c: number, d: number, e: number, f: number, g: number, h: number, i: number, j: number) => [number, number, number, number];
    readonly seal_aleth_payload: (a: number, b: number, c: number, d: number) => [number, number, number, number];
    readonly seal_aleth_v2: (a: number, b: number, c: number, d: number, e: number, f: number) => [number, number, number, number];
    readonly __wbindgen_exn_store: (a: number) => void;
    readonly __externref_table_alloc: () => number;
    readonly __wbindgen_externrefs: WebAssembly.Table;
    readonly __externref_table_dealloc: (a: number) => void;
    readonly __wbindgen_free: (a: number, b: number, c: number) => void;
    readonly __wbindgen_malloc: (a: number, b: number) => number;
    readonly __wbindgen_realloc: (a: number, b: number, c: number, d: number) => number;
    readonly __wbindgen_start: () => void;
}

export type SyncInitInput = BufferSource | WebAssembly.Module;

/**
 * Instantiates the given `module`, which can either be bytes or
 * a precompiled `WebAssembly.Module`.
 *
 * @param {{ module: SyncInitInput }} module - Passing `SyncInitInput` directly is deprecated.
 *
 * @returns {InitOutput}
 */
export function initSync(module: { module: SyncInitInput } | SyncInitInput): InitOutput;

/**
 * If `module_or_path` is {RequestInfo} or {URL}, makes a request and
 * for everything else, calls `WebAssembly.instantiate` directly.
 *
 * @param {{ module_or_path: InitInput | Promise<InitInput> }} module_or_path - Passing `InitInput` directly is deprecated.
 *
 * @returns {Promise<InitOutput>}
 */
export default function __wbg_init (module_or_path?: { module_or_path: InitInput | Promise<InitInput> } | InitInput | Promise<InitInput>): Promise<InitOutput>;
