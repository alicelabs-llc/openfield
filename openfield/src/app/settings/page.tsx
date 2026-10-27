"use client";

import { useState, useEffect, useCallback } from "react";
import {
  type StoredCredentials,
  encryptCredentials,
  decryptCredentials,
  loadEncryptedBlob,
  saveEncryptedBlob,
  clearEncryptedBlob,
  exportAsEnvFile,
  parseEnvFile,
} from "@/generation/secure-credentials";
import { PROVIDER_SIGNUPS } from "@/generation/provider-signups";

export default function SettingsPage() {
  const [passphrase, setPassphrase] = useState("");
  const [unlocked, setUnlocked] = useState(false);
  const [creds, setCreds] = useState<StoredCredentials>({});
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [hasStoredBlob, setHasStoredBlob] = useState(false);

  useEffect(() => {
    setHasStoredBlob(loadEncryptedBlob() !== null);
  }, []);

  const handleUnlock = useCallback(async () => {
    setError(null);
    setSuccess(null);
    const blob = loadEncryptedBlob();
    if (!blob) {
      // First time — just set unlocked so user can enter credentials
      setUnlocked(true);
      setSuccess("No saved credentials. Enter your API keys below and click Save.");
      return;
    }
    if (!passphrase) {
      setError("Enter your passphrase to unlock saved credentials.");
      return;
    }
    try {
      const decrypted = await decryptCredentials(blob, passphrase);
      setCreds(decrypted);
      setUnlocked(true);
      setSuccess("Credentials unlocked.");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Decryption failed.");
    }
  }, [passphrase]);

  const handleSave = useCallback(async () => {
    setError(null);
    setSuccess(null);
    if (!passphrase || passphrase.length < 6) {
      setError("Passphrase must be at least 6 characters.");
      return;
    }
    try {
      const blob = await encryptCredentials(creds, passphrase);
      saveEncryptedBlob(blob);
      setHasStoredBlob(true);
      setSuccess("Credentials saved (AES-GCM encrypted in this browser).");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Save failed.");
    }
  }, [creds, passphrase]);

  const handleClear = useCallback(() => {
    if (!confirm("This will permanently delete all saved credentials from this browser. Continue?")) {
      return;
    }
    clearEncryptedBlob();
    setCreds({});
    setPassphrase("");
    setUnlocked(false);
    setHasStoredBlob(false);
    setSuccess("All credentials cleared from this browser.");
  }, []);

  const handleExportEnv = useCallback(() => {
    if (Object.keys(creds).length === 0) {
      setError("No credentials to export.");
      return;
    }
    if (!confirm("This will download a .env file with your API keys in PLAINTEXT. Anyone with this file can use your keys. Continue?")) {
      return;
    }
    const env = exportAsEnvFile(creds);
    const blob = new Blob([env], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "openfield.env";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    setSuccess("Downloaded openfield.env — keep it private, do not commit to git.");
  }, [creds]);

  const handleImportEnv = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        try {
          const parsed = parseEnvFile(String(reader.result));
          setCreds((prev) => ({ ...prev, ...parsed }));
          setSuccess(`Imported ${Object.keys(parsed).length} credentials from .env file.`);
          setError(null);
        } catch (err) {
          setError("Could not parse .env file: " + (err instanceof Error ? err.message : "?"));
        }
      };
      reader.readAsText(file);
    },
    [],
  );

  const handleCopyToken = useCallback((value: string) => {
    navigator.clipboard.writeText(value);
    setSuccess("Token copied to clipboard.");
  }, []);

  const updateField = (field: keyof StoredCredentials, value: string) => {
    setCreds((prev) => ({ ...prev, [field]: value || undefined }));
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>🔑 OpenField — API Keys Settings</h1>
        <p style={styles.subtitle}>
          All credentials are stored encrypted (AES-GCM) in your browser&apos;s localStorage.
          A passphrase you choose protects them — without it, the data is unrecoverable.
        </p>
      </header>

      {/* Passphrase section */}
      <section style={styles.section}>
        <h2 style={styles.h2}>Passphrase</h2>
        <p style={styles.help}>
          Used to encrypt/decrypt your API keys locally. Pick a memorable one — there&apos;s no recovery.
        </p>
        <input
          type="password"
          value={passphrase}
          onChange={(e) => setPassphrase(e.target.value)}
          placeholder={hasStoredBlob ? "Enter your passphrase to unlock" : "Choose a passphrase (min 6 chars)"}
          style={styles.input}
          autoComplete="off"
        />
        <div style={styles.buttonRow}>
          {!unlocked ? (
            <button onClick={handleUnlock} style={styles.primaryBtn}>
              {hasStoredBlob ? "🔓 Unlock" : "🆕 Start"}
            </button>
          ) : (
            <>
              <button onClick={handleSave} style={styles.primaryBtn}>
                💾 Save encrypted
              </button>
              <button onClick={handleExportEnv} style={styles.ghostBtn}>
                📥 Download .env
              </button>
              <label style={styles.ghostBtn}>
                📤 Import .env
                <input
                  type="file"
                  accept=".env,.txt,text/plain"
                  onChange={handleImportEnv}
                  style={{ display: "none" }}
                />
              </label>
              <button onClick={handleClear} style={styles.dangerBtn}>
                🗑 Clear all
              </button>
            </>
          )}
        </div>
      </section>

      {error && (
        <div style={styles.alertError}>
          <strong>⚠️</strong> {error}
        </div>
      )}
      {success && !error && (
        <div style={styles.alertSuccess}>
          <strong>✓</strong> {success}
        </div>
      )}

      {/* Credentials grid */}
      {unlocked && (
        <section style={styles.section}>
          <h2 style={styles.h2}>API Keys</h2>
          <p style={styles.help}>
            Click a provider name to open their signup page in a new tab. Get a key, paste it below, click Save.
            Pollinations works without a key — others require one.
          </p>
          <div style={styles.grid}>
            {PROVIDER_SIGNUPS.map((provider) => {
              const field = provider.id as keyof StoredCredentials;
              const value = creds[field] ?? "";
              const isSet = Boolean(value);
              return (
                <div
                  key={provider.id}
                  style={{
                    ...styles.card,
                    borderColor: isSet ? "#3d8c40" : "rgba(255,255,255,0.15)",
                  }}
                >
                  <div style={styles.cardHeader}>
                    <div>
                      <a
                        href={provider.signupUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={styles.providerLink}
                      >
                        {provider.name} ↗
                      </a>
                      <div style={styles.blurb}>{provider.blurb}</div>
                    </div>
                    {isSet ? (
                      <span style={styles.badgeSet}>✓ Set</span>
                    ) : provider.required ? (
                      <span style={styles.badgeMissing}>Required</span>
                    ) : (
                      <span style={styles.badgeOptional}>Optional</span>
                    )}
                  </div>
                  <div style={styles.cardBody}>
                    <div style={styles.freeTierBox}>
                      <strong>Free tier:</strong> {provider.freeTier}
                    </div>
                    <div style={styles.tokenFormatRow}>
                      <strong>Token format:</strong>
                      <code style={styles.code}>{provider.tokenFormat}</code>
                    </div>
                    <div style={styles.inputRow}>
                      <input
                        type="password"
                        value={value}
                        onChange={(e) => updateField(field, e.target.value)}
                        placeholder={`Paste your ${provider.name} key here`}
                        style={styles.inputInline}
                        autoComplete="off"
                        spellCheck={false}
                      />
                      {isSet && (
                        <button
                          onClick={() => handleCopyToken(value)}
                          style={styles.iconBtn}
                          title="Copy"
                          type="button"
                        >
                          📋
                        </button>
                      )}
                    </div>
                    {provider.unlocksModels.length > 0 && (
                      <div style={styles.unlocksRow}>
                        <strong>Unlocks:</strong>{" "}
                        {provider.unlocksModels.map((m) => (
                          <span key={m} style={styles.modelChip}>
                            {m}
                          </span>
                        ))}
                      </div>
                    )}
                    {provider.docsUrl && (
                      <a
                        href={provider.docsUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={styles.docsLink}
                      >
                        📚 Docs
                      </a>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      )}

      <footer style={styles.footer}>
        <p style={styles.footerText}>
          ⚠️ <strong>Security:</strong> Credentials are AES-GCM encrypted with your passphrase before
          being saved. The passphrase is never stored. If you forget it, the data is unrecoverable.
          Clear browser data = clear all credentials.
        </p>
        <p style={styles.footerText}>
          <a href="/" style={styles.link}>← Back to studio</a>
        </p>
      </footer>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    backgroundColor: "#0a0a0b",
    color: "#e4e4e7",
    minHeight: "100vh",
    fontFamily: "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif",
    padding: "32px 24px 64px",
    maxWidth: 1200,
    margin: "0 auto",
  },
  header: { marginBottom: 32 },
  title: { fontSize: 28, fontWeight: 700, margin: 0, marginBottom: 8 },
  subtitle: { fontSize: 14, color: "#a0a0a8", margin: 0, lineHeight: 1.5 },
  section: {
    backgroundColor: "rgba(255,255,255,0.04)",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: 12,
    padding: 20,
    marginBottom: 24,
  },
  h2: { fontSize: 18, fontWeight: 600, margin: 0, marginBottom: 8 },
  help: { fontSize: 13, color: "#888894", margin: "0 0 12px", lineHeight: 1.5 },
  input: {
    width: "100%",
    padding: "12px 14px",
    backgroundColor: "rgba(0,0,0,0.4)",
    border: "1px solid rgba(255,255,255,0.12)",
    borderRadius: 8,
    color: "#fff",
    fontSize: 14,
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
    outline: "none",
  },
  buttonRow: { display: "flex", gap: 8, flexWrap: "wrap", marginTop: 12 },
  primaryBtn: {
    padding: "10px 18px",
    backgroundColor: "#3d8c40",
    color: "#fff",
    border: "none",
    borderRadius: 8,
    fontSize: 14,
    fontWeight: 600,
    cursor: "pointer",
  },
  ghostBtn: {
    padding: "10px 18px",
    backgroundColor: "transparent",
    color: "#e4e4e7",
    border: "1px solid rgba(255,255,255,0.2)",
    borderRadius: 8,
    fontSize: 14,
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
  },
  dangerBtn: {
    padding: "10px 18px",
    backgroundColor: "transparent",
    color: "#ff6b6b",
    border: "1px solid #ff6b6b40",
    borderRadius: 8,
    fontSize: 14,
    cursor: "pointer",
  },
  alertError: {
    backgroundColor: "rgba(255, 107, 107, 0.1)",
    border: "1px solid #ff6b6b",
    color: "#ff8585",
    padding: "12px 16px",
    borderRadius: 8,
    marginBottom: 16,
    fontSize: 14,
  },
  alertSuccess: {
    backgroundColor: "rgba(61, 140, 64, 0.1)",
    border: "1px solid #3d8c40",
    color: "#9ad99c",
    padding: "12px 16px",
    borderRadius: 8,
    marginBottom: 16,
    fontSize: 14,
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(340px, 1fr))",
    gap: 16,
  },
  card: {
    backgroundColor: "rgba(0,0,0,0.3)",
    border: "1px solid rgba(255,255,255,0.15)",
    borderRadius: 10,
    padding: 16,
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },
  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    gap: 8,
  },
  providerLink: {
    color: "#5fb8ff",
    fontSize: 16,
    fontWeight: 600,
    textDecoration: "none",
  },
  blurb: { fontSize: 12, color: "#888894", marginTop: 4, lineHeight: 1.4 },
  badgeSet: {
    fontSize: 11,
    padding: "3px 8px",
    backgroundColor: "#3d8c40",
    color: "#fff",
    borderRadius: 4,
    fontWeight: 600,
    whiteSpace: "nowrap",
  },
  badgeMissing: {
    fontSize: 11,
    padding: "3px 8px",
    backgroundColor: "#ff6b6b30",
    color: "#ff8585",
    borderRadius: 4,
    fontWeight: 600,
    whiteSpace: "nowrap",
  },
  badgeOptional: {
    fontSize: 11,
    padding: "3px 8px",
    backgroundColor: "#5fb8ff20",
    color: "#5fb8ff",
    borderRadius: 4,
    fontWeight: 600,
    whiteSpace: "nowrap",
  },
  cardBody: { display: "flex", flexDirection: "column", gap: 8 },
  freeTierBox: {
    fontSize: 12,
    color: "#b0b0b8",
    backgroundColor: "rgba(255,255,255,0.04)",
    padding: 8,
    borderRadius: 6,
    lineHeight: 1.5,
  },
  tokenFormatRow: { fontSize: 12, color: "#a0a0a8" },
  code: {
    display: "inline-block",
    marginLeft: 4,
    padding: "2px 6px",
    backgroundColor: "rgba(0,0,0,0.5)",
    borderRadius: 4,
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
    fontSize: 11,
    color: "#9ad99c",
  },
  inputRow: { display: "flex", gap: 6 },
  inputInline: {
    flex: 1,
    padding: "8px 10px",
    backgroundColor: "rgba(0,0,0,0.4)",
    border: "1px solid rgba(255,255,255,0.12)",
    borderRadius: 6,
    color: "#fff",
    fontSize: 13,
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
    outline: "none",
  },
  iconBtn: {
    padding: "8px 12px",
    backgroundColor: "rgba(255,255,255,0.06)",
    border: "1px solid rgba(255,255,255,0.12)",
    borderRadius: 6,
    cursor: "pointer",
    fontSize: 13,
  },
  unlocksRow: {
    fontSize: 12,
    color: "#a0a0a8",
    display: "flex",
    flexWrap: "wrap",
    gap: 4,
    alignItems: "center",
  },
  modelChip: {
    padding: "2px 6px",
    backgroundColor: "rgba(95, 184, 255, 0.1)",
    color: "#5fb8ff",
    borderRadius: 4,
    fontSize: 11,
  },
  docsLink: {
    color: "#888894",
    fontSize: 12,
    textDecoration: "none",
    alignSelf: "flex-start",
  },
  footer: {
    marginTop: 32,
    paddingTop: 16,
    borderTop: "1px solid rgba(255,255,255,0.08)",
  },
  footerText: {
    fontSize: 12,
    color: "#888894",
    margin: 0,
    marginBottom: 8,
    lineHeight: 1.5,
  },
  link: { color: "#5fb8ff", textDecoration: "none" },
};
