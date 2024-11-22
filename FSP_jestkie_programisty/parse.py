import requests
import certifi


def download_pdf_with_headers(url, save_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept": "application/pdf",
        "Referer": "https://google.com",  # Replace with the referer if needed
    }

    try:
        response = requests.get(url, headers=headers, stream=True,
                                verify="C:/Users/dan24/OneDrive/Рабочий стол/pydf/website.crt")  # Ignoring SSL for now
        response.raise_for_status()

        with open(save_path, 'wb') as pdf_file:
            for chunk in response.iter_content(chunk_size=8192):
                pdf_file.write(chunk)

        print(f"PDF downloaded successfully and saved to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download PDF: {e}")


# Example usage
pdf_url = "https://storage.minsport.gov.ru/cms-uploads/cms/II_chast_EKP_2024_14_11_24_65c6deea36.pdf"
save_location = "II_chast_EKP_2024_with_certificate.pdf"

download_pdf_with_headers(pdf_url, save_location)

# certificates needed (provided in websice.crt):
# GlobalSign Root R6
# GlobalSign GCC R6 AlphaSSL CA 2023