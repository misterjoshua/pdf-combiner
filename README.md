# PDF Combiner

PDF Combiner is a web application built with Streamlit that allows users to combine multiple PDF files and images into a single PDF document.

## Live Demo

You can try out the PDF Combiner here: [PDF Combiner App](https://pdf-combiner-nenkcbnsqwrnjt8apptvuyt.streamlit.app/)

## Features

- Upload multiple PDF files and images (JPG, JPEG, PNG)
- Reorder files before combining
- Convert images to PDF pages
- Download the combined PDF file

## How to Use

1. Visit the [PDF Combiner App](https://pdf-combiner-nenkcbnsqwrnjt8apptvuyt.streamlit.app/) in your web browser.
2. Click on "Choose files to combine" to upload your PDF files and/or images.
3. Drag and drop the files to reorder them as needed.
4. Click the "Combine PDFs" button to merge the files.
5. Once the process is complete, click "Download combined PDF" to save the result.

## Technical Details

This application is built using:
- Python
- Streamlit for the web interface
- PyPDF2 for PDF manipulation
- Reportlab for creating PDFs from images
- Pillow (PIL) for image processing

## Local Installation

To run this application locally:

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install streamlit PyPDF2 reportlab Pillow
   ```
3. Run the Streamlit app:
   ```
   streamlit run streamlit.py
   ```

## Contributing

Contributions to improve PDF Combiner are welcome. Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

