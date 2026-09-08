/**
 * validate-gate — harness-level enforcement for the company brain.
 *
 * Port of ml-python-base/.opencode/plugin/verify-gate.ts, reduced to what a
 * markdown knowledge base needs: there is no ruff/pytest layer, the only gate
 * is `make validate` (structure, links, IDs, work-unit frontmatter, index
 * freshness). Governance text ("run make validate") is advisory; a small
 * self-hosted build model will skip it. This plugin makes it mechanical.
 *
 * event:"session.idle" — when the agent finishes a turn, run `make validate`
 * and toast PASS/FAIL. Self-detects the brain (brain.config.json + AGENTS.md at
 * the root) so it never runs a foreign workspace's Makefile.
 *
 * `import type` is erased at runtime, so this file has no runtime dependency on
 * the @opencode-ai/plugin package.
 */
import { existsSync } from "node:fs";
import type { Plugin } from "@opencode-ai/plugin";

export const ValidateGate: Plugin = async ({ $, client, directory }) => {
  const run = (cmd: ReturnType<typeof $>) => cmd.cwd(directory).quiet().nothrow();
  const isBrain =
    existsSync(`${directory}/brain.config.json`) && existsSync(`${directory}/AGENTS.md`);

  return {
    event: async ({ event }) => {
      if (event.type !== "session.idle") return;
      if (!isBrain) return;
      const gate = await run($`make validate`);
      const passed = gate.exitCode === 0;
      try {
        await client.tui.showToast({
          body: {
            title: "validate-gate",
            message: passed
              ? "make validate passed ✅"
              : "make validate FAILED ❌ — the work is not done until this is green",
            variant: passed ? "success" : "error",
            duration: 6000,
          },
        });
      } catch {
        // TUI not attached (headless run): the gate still ran; ignore toast.
      }
    },
  };
};
