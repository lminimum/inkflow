export interface NavigationItem {
  to?: string
  icon?: any
  label?: string
  handler?: () => void
}

export interface ModelListResponse {
  [service: string]: string[];
}

export interface GenerateResponse {
  content: string;
  model?: string;
  timestamp?: number;
}