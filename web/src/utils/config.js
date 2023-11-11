/*
	机器人配置文件（由于）
	添加流程：
		先从Poe中找到机器人的名称
		再下载机器人头像到@/assets
		再复制机器人的描述
		最后在下面的preset中添加机器人的信息
*/
export default {
	preset: {
		Assistant: {
			avatar: "Assistant.svg",
			desc: "通用助手机器人，在编程相关任务和非英语语言方面有优势。由 gpt-3.5-turbo 提供支持。原名为 Sage。",
		},
		"Web-Search": {
			avatar: "Web-Search.jpeg",
			desc: "通用助手机器人，可以根据需要进行网络搜索以提供信息。特别适用于关于最新信息或具体事实的查询。由 gpt-3.5-turbo 提供支持。（目前处于测试发布阶段）",
		},
		"GPT-4": {
			avatar: "GPT-4.png",
			desc: "OpenAI 最强大的模型。在定量问题（数学和物理）、创意写作和许多其他具有挑战性的任务方面比 ChatGPT 更强。",
		},
		"DALL-E-3": {
			avatar: "DALL-E-3.jpeg",
			desc: "OpenAI最强大的图像生成模型。根据用户最近的提示生成具有复杂细节的高质量图像。",
		},
		StableDiffusionXL: {
			avatar: "StableDiffusionXL.jpeg",
			desc: "基于用户最近的提示生成高质量图像。用户可以使用提示末尾的 '--no' 参数指定要在图像中避免的元素（例如：'高树，白天 --no 雨'）。由 Stable Diffusion XL 提供支持。",
		},
		"Claude-instant-100k": {
			avatar: "Claude-instant-100k.png",
			desc: "Anthropic 最快的模型，具有增加的 100k Token（约 75,000 个单词）的上下文窗口。可以分析非常长的文档、代码等。",
		},
		"Claude-2-100k": {
			avatar: "Claude-2-100k.png",
			desc: "Anthropic 最强大的模型，具有增加的 100k Token（约 75,000 个单词）的上下文窗口。在创意写作方面特别擅长。",
		},
		"Claude-instant": {
			avatar: "Claude-instant.png",
			desc: "Anthropic 最快的模型，擅长创意任务。具有 9k Token（约 7,000 个单词）的上下文窗口。",
		},
		ChatGPT: {
			avatar: "ChatGPT.png",
			desc: "由 gpt-3.5-turbo 提供支持。",
		},
		"ChatGPT-16k": {
			avatar: "ChatGPT-16k.webp",
			desc: "由 gpt-3.5-turbo-16k 提供支持。由于这是一个测试模型，使用限制可能会发生变化。",
		},
		"GPT-4-32k": {
			avatar: "GPT-4-32k.webp",
			desc: "由 gpt-4-32k 提供支持。由于这是一个测试模型，使用限制可能会发生变化。",
		},
		"Google-PaLM": {
			avatar: "Google-PaLM.webp",
			desc: "由 Google 的 PaLM 2 chat-bison 模型提供支持。支持 8k Token 的上下文窗口。",
		},
		"Llama-2-70b": {
			avatar: "Llama-2-70b.webp",
			desc: "来自 Meta 的 Llama-2-70b-chat。",
		},
		"Code-Llama-34b": {
			avatar: "Code-Llama-34b.webp",
			desc: "来自 Meta 的 Code-Llama-34b-instruct。擅长生成和讨论代码，支持 16k Token 的上下文窗口。",
		},
		"Llama-2-13b": {
			avatar: "Llama-2-13b.webp",
			desc: "来自 Meta 的 Llama-2-13b-chat。",
		},
		"Llama-2-7b": {
			avatar: "Llama-2-7b.webp",
			desc: "来自 Meta 的 Llama-2-7b-chat。",
		},
		"Code-Llama-13b": {
			avatar: "Code-Llama-13b.webp",
			desc: "来自 Meta 的 Code-Llama-13b-instruct。擅长生成和讨论代码，支持 16k Token 的上下文窗口。",
		},
		"Code-Llama-7b": {
			avatar: "Code-Llama-7b.webp",
			desc: "来自 Meta 的 Code-Llama-7b-instruct。擅长生成和讨论代码，支持 16k Token 的上下文窗口。",
		},
		"Solar-0-70b": {
			avatar: "Solar-0-70b.webp",
			desc: "Solar-0-70b 是来自 Upstage 的一款顶级模型，在 HuggingFace Open LLM 排行榜上排名靠前，并且是 Llama 2 的微调版本。",
		},
		"GPT-3.5-Turbo-Instruct": {
			avatar: "GPT-3.5-Turbo-Instruct.png",
			desc: "GPT-3.5-Turbo-Instruct 是由 gpt-3.5-turbo-instruct 提供支持的模型。",
		},
		"GPT-3.5-Turbo": {
			avatar: "ChatGPT.png",
			desc: "由 gpt-3.5-turbo 提供支持。无系统Prompt。",
		},
		"fw-mistral-7b": {
			avatar: "fw-mistral-7b.jpeg",
			desc: "Bot powered by Fireworks.ai's hosted Mistral-7b-instruct model https://app.fireworks.ai/models/fireworks/mistral-7b-instruct-4k",
		},
	},
};
