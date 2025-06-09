import wave
import math
import struct

def gerar_som_aeromoca(nome_arquivo="aeromoca.wav", sample_rate=44100):
    volume = 0.5
    duracao_tom = 0.3  # 300ms por tom
    pausa_ms = 100
    n_silencio = int(sample_rate * (pausa_ms / 1000.0))
    freq_ding = 1200  # tom agudo
    freq_dong = 800   # tom grave

    def gerar_tom(freq, duracao):
        n_samples = int(sample_rate * duracao)
        return [
            int(volume * math.sin(2 * math.pi * freq * (i / sample_rate)) * 32767.0)
            for i in range(n_samples)
        ]

    som_ding = gerar_tom(freq_ding, duracao_tom)
    silencio = [0] * n_silencio
    som_dong = gerar_tom(freq_dong, duracao_tom)

    dados = som_ding + silencio + som_dong

    with wave.open(nome_arquivo, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, 0, "NONE", "not compressed"))
        for val in dados:
            wav_file.writeframesraw(struct.pack('<h', val))

    print(f"{nome_arquivo} gerado com sucesso!")

if __name__ == "__main__":
    gerar_som_aeromoca()
