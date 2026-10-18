# Privacy and credentials

The Python integrations send selected prompts, media inputs, model settings and your application API Key directly to `https://api.acedata.cloud`. They do not send requests to a proxy controlled by this repository. Tool schemas exclude the client credential; secrets are masked in representations. Do not place credentials in prompts or shared workflow exports. Optional LangSmith tracing is controlled by your application's environment and settings; review what your application records before enabling it.

The code does not download returned media. Store and share output URLs according to your own access controls. API calls use your current account balance, permissions and service prices. This project is provided by Ace Data Cloud and is not an official Suno, ByteDance, OpenAI or Google client.
