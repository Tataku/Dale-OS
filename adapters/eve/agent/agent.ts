import { defineAgent } from "eve";

export default defineAgent({
  model: process.env.DALE_OS_MODEL ?? "openai/gpt-5.4",
});
