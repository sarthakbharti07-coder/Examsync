
import { api } from "../lib/api";

export interface UploadedDocument {
  id: string;
  project_id: string;
  filename: string;
  file_size: number;
  status: string;
  message: string;
}

export const documentsApi = {
  async upload(
    projectId: string,
    file: File,
    onProgress?: (progress: number) => void,
  ): Promise<UploadedDocument> {
    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post<UploadedDocument>(
      "/documents/upload",
      formData,
      {
        params: {
          project_id: projectId,
        },

        onUploadProgress: (event) => {
          if (event.total && onProgress) {
            const progress = Math.round(
              (event.loaded / event.total) * 100,
            );

            onProgress(progress);
          }
        },
      },
    );

    return response.data;
  },
};
