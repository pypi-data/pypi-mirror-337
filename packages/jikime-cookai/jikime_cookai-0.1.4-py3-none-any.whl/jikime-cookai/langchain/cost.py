import os
from pydub import AudioSegment
import json
import tiktoken

class CostCalculator:
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        # 모델별 토큰 비용 상수 (USD 가격)
        self.gpt_4_turbo_input_cost = 10 / 1_000_000  
        self.gpt_4_turbo_output_cost = 30 / 1_000_000
        self.gpt_3_5_turbo_input_cost = 0.5 / 1_000_000
        self.gpt_3_5_turbo_output_cost = 1.5 / 1_000_000
        
        self.exchange_rate = 1400
        
        self.costs = {
            "GPT-4 Turbo": (self.gpt_4_turbo_input_cost, self.gpt_4_turbo_output_cost),
            "GPT-3.5 Turbo": (self.gpt_3_5_turbo_input_cost, self.gpt_3_5_turbo_output_cost)
        }

    def read_file_as_segments(self, file_path: str) -> list:
        """JSONL 파일에서 데이터를 읽어 세그먼트 리스트로 반환"""
        with open(file_path, "r") as file:
            return [json.loads(line) for line in file]

    def combine_speech_data(self, segments: list) -> str:
        """세그먼트 데이터를 텍스트로 결합"""
        return "\n".join(f"{item['label']}: {item['text']}" for item in segments)

    def calculate_token_costs(self, token_length: int, cost: float) -> float:
        """토큰 길이와 비용 정보를 바탕으로 총 비용을 계산"""
        return token_length * cost * self.exchange_rate * 1.1

    def summarize_costs(self, file_name: str, input_length: int, output_length: int):
        """비용 요약 및 출력"""
        print(f"{file_name}")
        print(f"input tokens: {input_length}")
        print(f"output tokens: {output_length}")
        
        for model, (input_cost, output_cost) in self.costs.items():
            input_cost_total = self.calculate_token_costs(input_length, input_cost)
            output_cost_total = self.calculate_token_costs(output_length, output_cost)
            print(f"{model} input cost: {input_cost_total} 원")
            print(f"{model} output cost: {output_cost_total} 원") 
            print(f"{model} total cost: {input_cost_total + output_cost_total} 원")
            
    def check_cost_gpt(self, file_dir: str, file_name: str, prompt: str) -> float:
        file_path = os.path.join(file_dir, file_name, f"{file_name}.jsonl")
        segments = self.read_file_as_segments(file_path)
        speechnote_data = self.combine_speech_data(segments)

        input_token_text = f"{prompt}\n\n{speechnote_data}"
        input_token_length = len(self.tokenizer.encode(input_token_text, disallowed_special=()))

        summary_file_path = os.path.join(file_dir, file_name, f"{file_name}_summary.txt")
        with open(summary_file_path, "r") as file:
            summary = file.read()
        output_token_length = len(self.tokenizer.encode(summary, disallowed_special=()))

        # 원화 환율 1400원을 가정하고 계산
        self.summarize_costs(file_name, input_token_length, output_token_length)
        return input_token_length + output_token_length
                
def check_cost_whisper(file_dir: str, file_name: str) -> float:
    whisper_cost = 0.006
    exchange_rate = 1400
    file_path = os.path.join(file_dir, file_name, f"{file_name}.mp3")
    audio = AudioSegment.from_file(file_path)
    audio_length = len(audio) / 1000.0
    total_cost = audio_length / 60.0 * whisper_cost * exchange_rate * 1.1
    print(f"{file_name}({audio_length} sec) : {total_cost}원")
    return total_cost