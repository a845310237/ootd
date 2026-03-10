import OSS from 'ali-oss'

// OSS configuration from environment variables
const ossConfig = {
  region: process.env.OSS_REGION || '',
  accessKeyId: process.env.OSS_ACCESS_KEY_ID || '',
  accessKeySecret: process.env.OSS_ACCESS_KEY_SECRET || '',
  bucket: process.env.OSS_BUCKET || '',
  authorizationV4: true,
}

// Check if OSS is properly configured
export const isOSSConfigured = () => {
  return !!(ossConfig.region && ossConfig.accessKeyId && ossConfig.accessKeySecret && ossConfig.bucket)
}

// Create OSS client instance
export const ossClient = isOSSConfigured()
  ? new OSS(ossConfig)
  : null

/**
 * Generate object key for OSS upload
 * @param filename - Original filename
 * @returns Object key in format: uploads/YYYY/MM/uuid-filename
 */
export function generateObjectKey(filename: string): string {
  const date = new Date()
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const { randomUUID } = require('crypto')
  const uuid = randomUUID()
  return `uploads/${year}/${month}/${uuid}-${filename}`
}

/**
 * Get public URL for an OSS object
 * @param objectKey - OSS object key
 * @returns Full URL to the object
 */
export function getPublicUrl(objectKey: string): string {
  if (!ossClient) return ''

  const { region, bucket } = ossConfig
  return `https://${bucket}.${region}.aliyuncs.com/${objectKey}`
}

export default ossClient
