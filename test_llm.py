import asyncio
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.frames.frames import LLMMessagesFrame

async def main():
    service = OpenAILLMService(
        api_key="none",
        base_url="https://opencode.ai/zen/v1",
        model="big-pickle"
    )
    
    async def run_frames():
        # OpenAILLMService.process_frame requires yielding frames in the context of a PipelineTask,
        # but we can try manually calling process_frame.
        frame = LLMMessagesFrame(messages=[{"role": "user", "content": "hi"}])
        async for result_frame in service.process_frame(frame):
            print("Received:", result_frame)
            
    await run_frames()

asyncio.run(main())
