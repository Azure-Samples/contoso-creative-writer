import React, { useState } from "react";
import axios from "axios";
import { image_endpoint } from "../constants";
import "./spinner.css";

const ImageUpload = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploadStatus, setUploadStatus] = useState<string>("");
    const [isProcessing, setIsProcessing] = useState<boolean>(false); // New state for processing
    const [uploadLocation, setUploadLocation] = useState<string>("");
    const [uploadSafety, setUploadSafety] = useState<string>("");

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            setSelectedFile(event.target.files[0]);
        }
    };

    const url = `${
        image_endpoint.endsWith("/") ? image_endpoint : image_endpoint + "/"
      }api/upload-image`;

    const handleUpload = async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append("file", selectedFile);

        setIsProcessing(true); // Start processing
        setUploadStatus("");

        try {
            const response = await axios.post(url , formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });
            setUploadStatus(`Upload successful! ${response.data.message}`);
            setUploadLocation(`../../public/${response.data.filename}`);
            setUploadSafety(`${response.data.safety}`);
        } catch (error) {
            setUploadStatus("Upload failed. Please try again.");
            console.error("Error uploading file:", error);
        } finally {
            setIsProcessing(false); // End processing
        }
    };

    return (
        <div className="pt-4">
            <input type="file" onChange={handleFileChange} />
            <button
                type="button"
                className="flex flex-row gap-3 items-center rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                onClick={handleUpload}
            >
                Upload Image
            </button>
            {isProcessing && (
                <div className="flex items-center gap-2 mt-2">
                    <div className="loader" /> {/* Spinner */}
                    <p>Evaluating Image...</p>
                </div>
            )}
            {uploadStatus && <p>{uploadStatus}</p>}
            <p></p>
            {uploadSafety.length > 0 ? (
            uploadStatus && <img 
                    src={uploadLocation} 
                    alt="Uploaded content" 
                    style={{ maxWidth: "100%", height: "auto", border: "1px solid #ccc" }} 
                    />
            ) : (
            <p></p>
            )}
        </div>
    );
};

export default ImageUpload;
