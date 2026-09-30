// Smoke test for the new TS v2 seal/recover/migrate functions.
// Run with: npx tsx /tmp/alethech-test-v2-seal.ts

import { sealAlethV2, openAlethV2, recoverAlethV2, migrateAlethV1ToV2 } from "/home/z/my-project/alethech-publish-2/alethech-ts/aleth-container-v2.ts";
import { sealAlethPayload } from "/home/z/my-project/alethech-publish-2/alethech-ts/aleth-container.ts";
import { randomBytes } from "node:crypto";
import { readFileSync, mkdirSync, rmSync } from "node:fs";

const payload = {
  payload_version: 1,
  files: {
    "HEAD": Buffer.from("test-head").toString("base64url"),
    "commits/test.json": Buffer.from(JSON.stringify({ type: "MemoryCommit", version: 1 })).toString("base64url"),
  },
};

const tmpDir = "/tmp/alethech-ts-v2-test";
try { rmSync(tmpDir, { recursive: true, force: true }); } catch {}
mkdirSync(tmpDir, { recursive: true });

const v2File = tmpDir + "/test.aleth";

async function main() {
  console.log("=== 1. sealAlethV2 ===");
  const recoverySecret = randomBytes(32);
  const sealResult = await sealAlethV2(payload, v2File, "test-pass", {
    recoverySecret,
  });
  console.log("recoveryCode:", sealResult.recoveryCode);
  console.log("containerId:", sealResult.containerId);
  console.log("file size:", readFileSync(v2File).length, "bytes");

  console.log("");
  console.log("=== 2. openAlethV2 with passphrase ===");
  const opened = await openAlethV2(v2File, { passphrase: "test-pass" });
  console.log("container_id:", opened.container_id);
  console.log("slot_types:", opened.slot_types);
  console.log("payload keys:", Object.keys(opened.payload.files));

  console.log("");
  console.log("=== 3. openAlethV2 with recovery code ===");
  const openedR = await openAlethV2(v2File, { recovery_code: sealResult.recoveryCode as string });
  console.log("container_id:", openedR.container_id);
  console.log("slot_types:", openedR.slot_types);
  console.log("payloads match:", JSON.stringify(opened.payload) === JSON.stringify(openedR.payload));

  console.log("");
  console.log("=== 4. recoverAlethV2 (new passphrase, no rotate) ===");
  const recoveredFile = tmpDir + "/recovered.aleth";
  const recoverResult = await recoverAlethV2(v2File, recoveredFile, sealResult.recoveryCode as string, "new-pass");
  console.log("recoveryCode (same):", recoverResult.recoveryCode === sealResult.recoveryCode);
  console.log("containerId (same):", recoverResult.containerId === sealResult.containerId);

  console.log("");
  console.log("=== 5. openAlethV2 recovered ===");
  const openedRecovered = await openAlethV2(recoveredFile, { passphrase: "new-pass" });
  console.log("container_id matches:", openedRecovered.container_id === sealResult.containerId);
  console.log("payloads match:", JSON.stringify(openedRecovered.payload) === JSON.stringify(opened.payload));

  console.log("");
  console.log("=== 6. recoverAlethV2 with rotateRecovery ===");
  const rotatedFile = tmpDir + "/rotated.aleth";
  const rotateResult = await recoverAlethV2(v2File, rotatedFile, sealResult.recoveryCode as string, "new-pass-2", { rotateRecovery: true });
  console.log("recoveryCode changed:", rotateResult.recoveryCode !== sealResult.recoveryCode);
  const openedRotated = await openAlethV2(rotatedFile, { recovery_code: rotateResult.recoveryCode });
  console.log("rotated payload matches:", JSON.stringify(openedRotated.payload) === JSON.stringify(opened.payload));

  console.log("");
  console.log("=== 7. migrateAlethV1ToV2 ===");
  // First create a v1 container
  const v1File = tmpDir + "/v1.aleth";
  await sealAlethPayload(payload, v1File, "old-pass");
  console.log("v1 file created, size:", readFileSync(v1File).length);
  // Now migrate
  const migratedFile = tmpDir + "/migrated.aleth";
  const migrateResult = await migrateAlethV1ToV2(v1File, migratedFile, "old-pass", "migrated-pass");
  console.log("migrated containerId:", migrateResult.containerId);
  console.log("migrated recoveryCode:", migrateResult.recoveryCode);
  // Open migrated
  const openedMigrated = await openAlethV2(migratedFile, { passphrase: "migrated-pass" });
  // Compare by sorting keys (JCS sorts, so the order may differ from input)
  const sortPayload = (p: any) => JSON.stringify(p, Object.keys(p).sort());
  console.log("migrated payload matches:", sortPayload(openedMigrated.payload) === sortPayload(payload));

  console.log("");
  console.log("=== ALL TS TESTS PASSED ===");
}

main().catch(e => {
  console.error("TEST FAILED:", e.message);
  console.error(e.stack);
  process.exit(1);
});
