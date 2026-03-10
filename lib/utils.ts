import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Safe JSON parse for arrays stored as strings in database
export function parseJsonArray<T>(value: string | null | undefined, defaultValue: T[]): T[] {
  if (!value) return defaultValue
  try {
    const parsed = JSON.parse(value)
    return Array.isArray(parsed) ? parsed : defaultValue
  } catch {
    return defaultValue
  }
}

// Safe JSON stringify for arrays
export function stringifyJsonArray<T>(value: T[] | null | undefined): string | null {
  if (!value || value.length === 0) return null
  return JSON.stringify(value)
}
