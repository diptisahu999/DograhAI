import { getSignedUrlApiV1S3SignedUrlGet } from "@/client/sdk.gen";

/**
 * Get a signed URL and download a file
 */
export async function downloadFile(url: string | null) {
    if (!url) return;

    try {
        const response = await getSignedUrlApiV1S3SignedUrlGet({
            query: {
                key: url
            },
        });

        if (response.data?.url) {
            window.open(response.data.url, '_blank');
        }
    } catch (error) {
        console.error('Error downloading file:', error);
    }
}

/**
 * Return a signed URL for a given S3 key without triggering a download.
 * Useful for previewing media (audio or transcript) in-browser first.
 */
export async function getSignedUrl(url: string | null, inline: boolean = false): Promise<string | null> {
    if (!url) return null;

    try {
        const response = await getSignedUrlApiV1S3SignedUrlGet({
            query: {
                key: url,
                inline: inline,
            },
        });

        if (response.data?.url) {
            return response.data.url as string;
        }
    } catch (error) {
        console.error('Error getting signed URL:', error);
    }
    return null;
}
