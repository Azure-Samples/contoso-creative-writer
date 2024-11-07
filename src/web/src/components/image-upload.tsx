import React, { useState } from "react";
import axios from "axios";
import { image_endpoint } from "../constants";
import { setUploadLocation } from "../constants";

const ImageUpload = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploadStatus, setUploadStatus] = useState<string>("");

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

        try {
            const response = await axios.post(url , formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });
            setUploadStatus(`Upload successful! File location: ${response.data.location}`);
            const location = response.data.location;
            setUploadLocation(location); 
        } catch (error) {
            setUploadStatus("Upload failed. Please try again.");
            console.error("Error uploading file:", error);
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} />
            <button 
            type="button"
            className="flex flex-row gap-3 items-center rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
            onClick={handleUpload}>Upload Image</button>
            {uploadStatus && <p>{uploadStatus}</p>}
        </div>
    );
};

export default ImageUpload;
