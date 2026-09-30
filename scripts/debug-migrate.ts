import { openAleth, sealAlethPayload } from "/home/z/my-project/alethech-publish-2/alethech-ts/aleth-container.ts";
import { openAlethV2, migrateAlethV1ToV2 } from "/home/z/my-project/alethech-publish-2/alethech-ts/aleth-container-v2.ts";
import { mkdirSync, rmSync } from "node:fs";

const payload = {
  payload_version: 1,
  files: {
    "HEAD": Buffer.from("test-head").toString("base64url"),
    "commits/test.json": Buffer.from(JSON.stringify({ type: "MemoryCommit", version: 1 })).toString("base64url"),
  },
};

const tmpDir = "/tmp/alethech-debug-migrate";
try { rmSync(tmpDir, { recursive: true, force: true }); } catch {}
mkdirSync(tmpDir, { recursive: true });

async function main() {
  const v1File = tmpDir + "/v1.aleth";
  await sealAlethPayload(payload, v1File, "old-pass");

  const opened1 = await openAleth(v1File, "old-pass");
  console.log("v1 opened payload:");
  console.log(JSON.stringify(opened1.payload, null, 2));
  console.log("");

  const migratedFile = tmpDir + "/migrated.aleth";
  const result = await migrateAlethV1ToV2(v1File, migratedFile, "old-pass", "migrated-pass");
  console.log("migrate result:", result);

  const opened2 = await openAlethV2(migratedFile, { passphrase: "migrated-pass" });
  console.log("");
  console.log("v2 opened payload:");
  console.log(JSON.stringify(opened2.payload, null, 2));
  console.log("");
  console.log("original payload:");
  console.log(JSON.stringify(payload, null, 2));
}

main().catch(e => {
  console.error("FAILED:", e.message);
  process.exit(1);
});
