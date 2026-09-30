import { openAlethV2 } from "/home/z/my-project/alethech-publish-2/alethech-ts/aleth-container-v2.ts";

async function main() {
  console.log("=== TS opens Python-sealed v2 container ===");
  const r1 = await openAlethV2("/tmp/alethech-ts-v2-test/py-sealed.aleth", { passphrase: "py-pass" });
  console.log("opened by passphrase:");
  console.log("  container_id:", r1.container_id);
  console.log("  slot_types:", r1.slot_types);
  console.log("  files:", Object.keys(r1.payload.files));
  console.log("  payload matches expected:", r1.payload.files["HEAD"] === "dGVzdC1oZWFk");
}

main().catch(e => { console.error("FAIL:", e.message); process.exit(1); });
