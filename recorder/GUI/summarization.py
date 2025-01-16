from transformers import T5Tokenizer, AutoModelForSeq2SeqLM
import os
import torch
import os

def count_characters_in_file(file_path):
    """
    Zlicza liczbę znaków w pliku tekstowym.

    Args:
        file_path (str): Ścieżka do pliku tekstowego.

    Returns:
        int: Liczba znaków w pliku lub None, jeśli plik nie istnieje.
    """
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            return len(content)
    except Exception as e:
        print(f"Błąd podczas odczytu pliku: {e}")
        return None

def summarize_text(file_path, language="english"):
    """
    Streszcza tekst z pliku, uwzględniając język i zapisuje streszczenie do pliku.

    Args:
        file_path (str): Ścieżka do pliku tekstowego.
        language (str, optional): Język streszczenia ("english" lub "polish"). Defaults to "english".

    Returns:
       str: Ścieżka do pliku ze streszczeniem lub komunikat o błędzie.
    """
    count_letters = count_characters_in_file(file_path)
    if count_letters is None:
        return "Błąd: Plik nie istnieje."
    min_length=count_letters // 4
    max_length=count_letters // 2
    if not os.path.exists(file_path):
        return f"Błąd: Plik '{file_path}' nie istnieje."

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
    except Exception as e:
        return f"Błąd odczytu pliku: {e}"

    if language == "polish":
        model_name = "google/mt5-small"
        prefix = "streszcz po polsku: "
    elif language == "english":
        model_name = "google/mt5-small"
        prefix = "summarize in english: "
    else:
        return "Błąd: Nieobsługiwany język. Wybierz 'english' lub 'polish'."

    try:
        tokenizer = T5Tokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        if torch.cuda.is_available():
            model = model.to("cuda")
        
        # Dodanie prefiksu do tekstu
        text_with_prefix = prefix + text

        inputs = tokenizer(text_with_prefix, return_tensors="pt", truncation=False)
        if torch.cuda.is_available():
            inputs = inputs.to("cuda")

        summary_ids = model.generate(inputs["input_ids"],
                                    min_length=min_length,
                                    max_length=max_length,
                                    num_beams=4,
                                    early_stopping=True)

        summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True)[0]

        # Zapis do pliku
        base_name, ext = os.path.splitext(file_path)
        output_file_path = f"{base_name}_sum.txt"
        with open(output_file_path, "w", encoding="utf-8") as outfile:
           outfile.write(summary)
        return output_file_path
    except Exception as e:
        return f"Błąd podczas streszczania: {e}"

if __name__ == '__main__':
     # Stwórzmy przykładowe pliki jeśli nie istnieją
    if not os.path.exists("polski.txt"):
        with open("polski.txt", "w", encoding="utf-8") as f:
            f.write("To jest przykładowy tekst po polsku. Chcemy go podsumować.")
    if not os.path.exists("angielski.txt"):
        with open("angielski.txt", "w", encoding="utf-8") as f:
            f.write("This is an example text in English. We want to summarize it.")

    file_path = "polski.txt"
    language = "polish"
    output_file = summarize_text(file_path, language)
    if isinstance(output_file, str) and not "Błąd" in output_file :
        print(f"Streszczenie (język: {language}) zapisano do pliku: {output_file}")
    else:
        print(output_file)
    

    file_path = "angielski.txt"
    language = "english"
    output_file = summarize_text(file_path, language)
    if isinstance(output_file, str) and not "Błąd" in output_file:
       print(f"Streszczenie (język: {language}) zapisano do pliku: {output_file}")
    else:
        print(output_file)