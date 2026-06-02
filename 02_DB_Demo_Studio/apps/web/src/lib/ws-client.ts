// lib/ws-client.ts — WebSocket 客户端封装
// 连接管理 / 心跳 / 自动重连 / 事件路由

import type { WsClientEvent, WsServerEvent } from './types'

type EventHandler = (event: WsServerEvent) => void
type StatusHandler = (status: ConnectionStatus) => void

export type ConnectionStatus = 'connecting' | 'connected' | 'disconnected'

const RECONNECT_DELAYS = [1000, 2000, 4000, 8000]
const PING_INTERVAL = 30000

export class WsClient {
  private ws: WebSocket | null = null
  private teacherId: string
  private convId: string
  private handlers: Set<EventHandler> = new Set()
  private statusHandlers: Set<StatusHandler> = new Set()
  private reconnectAttempt = 0
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private pingTimer: ReturnType<typeof setInterval> | null = null
  private _status: ConnectionStatus = 'disconnected'
  private intentionalClose = false

  constructor(teacherId: string, convId: string) {
    this.teacherId = teacherId
    this.convId = convId
  }

  get status() { return this._status }

  private setStatus(s: ConnectionStatus) {
    this._status = s
    this.statusHandlers.forEach(h => h(s))
  }

  connect() {
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) return
    this.intentionalClose = false
    this.setStatus('connecting')

    // Use /ws path which Vite proxies to the backend
    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:'
    const url =
      `${protocol}//${location.host}/ws/chat` +
      `?teacher_id=${encodeURIComponent(this.teacherId)}` +
      `&conv_id=${encodeURIComponent(this.convId)}`
    this.ws = new WebSocket(url)

    this.ws.onopen = () => {
      this.setStatus('connected')
      this.reconnectAttempt = 0
      this.startPing()
    }

    this.ws.onmessage = (evt: MessageEvent) => {
      try {
        const event: WsServerEvent = JSON.parse(evt.data)
        this.handlers.forEach(h => h(event))
      } catch { /* skip parse errors */ }
    }

    this.ws.onclose = () => {
      this.stopPing()
      this.setStatus('disconnected')
      if (!this.intentionalClose) this.scheduleReconnect()
    }

    this.ws.onerror = () => { /* onclose will fire after this */ }
  }

  disconnect() {
    this.intentionalClose = true
    this.stopPing()
    this.clearReconnect()
    if (this.ws) { this.ws.close(); this.ws = null }
    this.setStatus('disconnected')
  }

  send(event: WsClientEvent) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(event))
    } else {
      console.warn('[WS] not connected, dropping:', event.type)
    }
  }

  onEvent(handler: EventHandler): () => void {
    this.handlers.add(handler)
    return () => this.handlers.delete(handler)
  }

  onStatusChange(handler: StatusHandler): () => void {
    this.statusHandlers.add(handler)
    return () => this.statusHandlers.delete(handler)
  }

  /** Update the convId and trigger a reconnect */
  public updateConvId(convId: string) {
    if (this.convId === convId) return
    this.convId = convId
    this.disconnect()
    this.connect()
  }

  private startPing() {
    this.stopPing()
    this.pingTimer = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'ping' }))
      }
    }, PING_INTERVAL)
  }

  private stopPing() {
    if (this.pingTimer) { clearInterval(this.pingTimer); this.pingTimer = null }
  }

  private scheduleReconnect() {
    this.clearReconnect()
    const delay = RECONNECT_DELAYS[Math.min(this.reconnectAttempt, RECONNECT_DELAYS.length - 1)]
    this.reconnectAttempt++
    console.log(`[WS] reconnecting in ${delay}ms (attempt ${this.reconnectAttempt})`)
    this.reconnectTimer = setTimeout(() => this.connect(), delay)
  }

  private clearReconnect() {
    if (this.reconnectTimer) { clearTimeout(this.reconnectTimer); this.reconnectTimer = null }
  }
}
