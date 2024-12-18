#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { exec } from "child_process";
import util from "util";

const execPromise = util.promisify(exec);

const server = new Server(
  {
    name: "list-server",
    version: "0.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "run_ls_or_dir",
        description: "Run the 'ls' command on Linux/macOS or 'dir' on Windows",
        inputSchema: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "The directory path to list files for",
            },
          },
          required: ["path"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name !== "run_ls_or_dir") {
    throw new Error("Unknown tool");
  }

  const path = String(request.params.arguments?.path);
  if (!path) {
    throw new Error("Path is required");
  }

  const command = process.platform === "win32" ? `dir ${path}` : `ls ${path}`;

  try {
    const { stdout } = await execPromise(command);
    return {
      content: [
        {
          type: "text",
          text: stdout,
        },
      ],
    };
  } catch (err) {
    const error = err as Error;
    return {
      content: [
        {
          type: "text",
          text: `Error executing command: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error("Server error:", (error as Error).message);
  process.exit(1);
});
