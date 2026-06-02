// hooks/useWebSocket.ts
// React WebSocket hook — 自动连接/重连/事件分发

import { useEffect, useRef, useCallback, useState, useMemo } from 'react'
import { WsClient, type ConnectionStatus } from '../lib/ws-client'
import type { WsClientEvent, WsServerEvent } from '../lib/types'
import { useConversationStore } from '../stores/conversationStore'
import { useDemoStore } from '../stores/demoStore'

export function useWebSocket(teacherId: string, convId: string) {
  const [status, setStatus] = useState<ConnectionStatus>('disconnected')
  const clientRef = useRef<WsClient | null>(null)
  // Stable references to handlers
  const convHandlerRef = useRef(useConversationStore.getState().handleServerEvent)
  const demoHandlerRef = useRef(useDemoStore.getState().handleServerEvent)

  // Keep handlers updated
  useEffect(() => {
    convHandlerRef.current = useConversationStore.getState().handleServerEvent
  })
  useEffect(() => {
    demoHandlerRef.current = useDemoStore.getState().handleServerEvent
  })

  // Unique session key — when teacherId or convId changes, we tear down and recreate
  const sessionKey = useMemo(() => `${teacherId}:${convId}`, [teacherId, convId])

  useEffect(() => {
    // Don't connect without a valid convId
    if (!convId) return

    const client = new WsClient(teacherId, convId)
    clientRef.current = client

    const unsubStatus = client.onStatusChange(setStatus)
    const unsubEvent = client.onEvent((event: WsServerEvent) => {
      convHandlerRef.current(event)
      demoHandlerRef.current(event)
    })

    client.connect()

    return () => {
      unsubStatus()
      unsubEvent()
      client.disconnect()
      clientRef.current = null
    }
  }, [sessionKey, convId]) // eslint-disable-line react-hooks/exhaustive-deps

  const send = useCallback((event: WsClientEvent) => {
    clientRef.current?.send(event)
  }, [])

  return { status, send, client: clientRef.current }
}
