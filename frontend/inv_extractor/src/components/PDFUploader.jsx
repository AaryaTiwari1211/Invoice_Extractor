import React, { useState } from 'react';
import axios from 'axios';

const PDFUploader = () => {
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleFileUpload = async () => {
        if (!selectedFile) return;

        try {
            const formData = new FormData();
            formData.append('pdf_file', selectedFile);

            // Upload the PDF file to the Django REST API
            const response = await axios.post('http://localhost:8000/api/process_pdf/', formData, {
                responseType: 'arraybuffer', // Set response type to 'arraybuffer' for binary data
            });

            // Process the PDF document and generate QR code
            const pdfData = response.data;
            // Call the Luxmi functions here using 'pdfData' if required

            // Create a Blob from the binary data received
            const pdfBlob = new Blob([pdfData], { type: 'application/pdf' });

            // Create a URL for the Blob
            const pdfUrl = URL.createObjectURL(pdfBlob);

            // Create an anchor tag to initiate the download
            const downloadLink = document.createElement('a');
            downloadLink.href = pdfUrl;
            downloadLink.download = 'merged_pdf_with_qr_code.pdf'; // Set the filename for the download
            downloadLink.click();

            // Clean up the URL after download
            URL.revokeObjectURL(pdfUrl);

            console.log('PDF Document uploaded successfully:', pdfData);
        } catch (error) {
            console.error('Error uploading PDF Document:', error);
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleFileUpload}>Upload PDF</button>
        </div>
    );
};

export default PDFUploader;
