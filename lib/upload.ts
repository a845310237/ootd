import { randomUUID } from 'crypto'
import { ossClient, generateObjectKey, getPublicUrl, isOSSConfigured } from './oss'

// Allowed image file types
const ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif']
const MAX_FILE_SIZE = 10 * 1024 * 1024 // 10MB

export interface UploadResult {
  success: boolean
  url?: string
  error?: string
}

/**
 * Upload image to OSS (阿里云对象存储)
 * Falls back to local storage if OSS is not configured
 */
export async function uploadImage(file: File | Blob, filename?: string): Promise<UploadResult> {
  try {
    // Validate file type
    const fileType = file instanceof File ? file.type : 'image/jpeg'
    if (!ALLOWED_TYPES.includes(fileType)) {
      return {
        success: false,
        error: `Invalid file type. Allowed types: ${ALLOWED_TYPES.join(', ')}`
      }
    }

    // Validate file size
    if (file.size > MAX_FILE_SIZE) {
      return {
        success: false,
        error: `File size exceeds limit of ${MAX_FILE_SIZE / 1024 / 1024}MB`
      }
    }

    // Generate unique filename
    const originalName = filename || (file instanceof File ? file.name : 'upload.jpg')

    // Convert file to buffer
    const bytes = await file.arrayBuffer()
    const buffer = Buffer.from(bytes)

    // Try OSS upload first
    if (isOSSConfigured() && ossClient) {
      try {
        const objectKey = generateObjectKey(originalName)
        const result = await ossClient.put(objectKey, buffer, {
          headers: {
            'Content-Type': fileType,
          },
        })

        return {
          success: true,
          url: result.url || getPublicUrl(objectKey)
        }
      } catch (ossError) {
        console.error('OSS upload error, falling back to local storage:', ossError)
        // Fall through to local storage
      }
    }

    // Fallback to local storage if OSS is not configured or upload failed
    return await uploadToLocal(buffer, originalName)
  } catch (error) {
    console.error('Upload error:', error)
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Upload failed'
    }
  }
}

/**
 * Upload to local storage (fallback)
 */
async function uploadToLocal(buffer: Buffer, filename: string): Promise<UploadResult> {
  const { writeFile, mkdir } = await import('fs/promises')
  const { join } = await import('path')
  const { existsSync } = await import('fs')

  const UPLOAD_DIR = process.env.UPLOAD_DIR || '/data/public/uploads'

  // Ensure upload directory exists
  if (!existsSync(UPLOAD_DIR)) {
    await mkdir(UPLOAD_DIR, { recursive: true })
  }

  // Generate unique filename
  const uniqueFilename = `${randomUUID()}-${filename}`
  const filepath = join(UPLOAD_DIR, uniqueFilename)

  // Save file
  await writeFile(filepath, buffer)

  // Return relative URL path
  return {
    success: true,
    url: `/uploads/${uniqueFilename}`
  }
}

export function getImageUrl(url: string | null): string {
  if (!url) return '/placeholder-clothing.jpg'
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  return url
}
