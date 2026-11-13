import { fileURLToPath } from 'node:url';
import { runLint, LintConsoleReporter } from '@microsoft/vally';

// Match the marketplace's static skill checks; do not execute agents or tools.
const rootPath = fileURLToPath(new URL('../../skills/', import.meta.url));
const result = await runLint({ rootPath });
await new LintConsoleReporter({ verbose: true, stream: process.stdout }).report(result);
if (!result.passed) process.exitCode = 1;
