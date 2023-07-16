import { useState } from 'react'
import React from 'react';
import PDFUploader from './components/PDFUploader';

const App = () => {
  return (
    <div>
      <h1>Invoice Extractor and Bar-Code Generator</h1>
      <PDFUploader />
    </div>
  );
};

export default App;
