"""Constants for the Liebherr integration."""

DOMAIN = "liebherr"
BASE_URL = "https://home-api.smartdevice.liebherr.com"
API_VERSION = "/v1"
BASE_API_URL = f"{BASE_URL}{API_VERSION}/devices"

DOOR_ALARM = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHZpZXdCb3g9IjAgMCA4MDAgODAwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1saW5lY2FwPSJzcXVhcmUiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS1taXRlcmxpbWl0PSIxLjUiIHhtbG5zOnY9Imh0dHBzOi8vdmVjdGEuaW8vbmFubyI+PHBhdGggZD0iTS4wMDItLjAwMWg4MDAuMDAxdjgwMEguMDAyeiIgZmlsbD0iI2QwMDAwMCIvPjxnIHRyYW5zZm9ybT0ibWF0cml4KDEuNDI4NzUgMCAwIDEuNDI4NzUgLTIyOS44NDEgLTg3LjI5NjMpIj48cGF0aCBkPSJNNTQyLjA5NyAxMTQuMTgxdjM0Mi43OTdMMzM5LjU2MiA0NzMuNjdWMTMwLjg3M2wyMDIuNTM1LTE2LjY5MnoiIGZpbGw9IiNkMDAwMDAiLz48cGF0aCBkPSJNNTQyLjA5NyAxMTQuMTgxdjM0Mi43OTdMMzM5LjU2MiA0NzMuNjdWMTMwLjg3M2wyMDIuNTM1LTE2LjY5MnptLTEwLjQ5OSAxMS4zOTlsLTE4MS41MzcgMTQuOTYydjMyMS43MjlsMTgxLjUzNy0xNC45NjJWMTI1LjU4eiIgZmlsbD0iI2ZmZiIvPjxwYXRoIGQ9Ik01NDIuMTA0IDExMy44NTV2MzQ3LjA2NkwzOTMuNjgxIDU2OC4yNzNWMjIxLjIwN2wxNDguNDIzLTEwNy4zNTJ6IiBmaWxsPSIjZDAwMDAwIi8+PHBhdGggZD0iTTU0Mi4xMDQgMTEzLjg1NXYzNDcuMDY2TDM5My42ODEgNTY4LjI3M1YyMjEuMjA3bDE0OC40MjMtMTA3LjM1MnptLTEwLjQ5OSAyMC41NTFMNDA0LjE4IDIyNi41N3YzMjEuMTUybDEyNy40MjUtOTIuMTY1VjEzNC40MDV6IiBmaWxsPSIjZmZmIi8+PHBhdGggZD0iTTQyNy41MjUgMzA3LjExM3Y3OC42MzEiIGZpbGw9Im5vbmUiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxMC41Ii8+PC9nPjwvc3ZnPg=="
AIR_FILTER = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHZpZXdCb3g9IjAgMCA4MDAgODAwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS1taXRlcmxpbWl0PSIyIiB4bWxuczp2PSJodHRwczovL3ZlY3RhLmlvL25hbm8iPjxwYXRoIGQ9Ik0uMDAyLS4wMDFoODAwLjAwMXY4MDBILjAwMnoiIGZpbGw9IiNkMDVjMDAiLz48ZyB0cmFuc2Zvcm09Im1hdHJpeCgxLjQyODc1IDAgMCAxLjQyODc1IC0yNzQuOTUgLTg3LjI5NjMpIj48cGF0aCBkPSJNNDIzLjExOSAxMTMuODU1djM0Ny4wNjZMMjc0LjY5NiA1NjguMjczVjIyMS4yMDdsMTQ4LjQyMy0xMDcuMzUyeiIgZmlsbD0iI2QwNWMwMCIvPjxwYXRoIGQ9Ik00MjMuMTE5IDExMy44NTV2MzQ3LjA2NkwyNzQuNjk2IDU2OC4yNzNWMjIxLjIwN2wxNDguNDIzLTEwNy4zNTJ6bS0xMC40OTkgMjAuNTUxTDI4NS4xOTUgMjI2LjU3djMyMS4xNTJsMTI3LjQyNS05Mi4xNjVWMTM0LjQwNXoiIGZpbGw9IiNmZmYiLz48cGF0aCBkPSJNNDcyLjExMiAxMTMuODU1djM0Ny4wNjZMMzIzLjY4OSA1NjguMjczVjIyMS4yMDdsMTQ4LjQyMy0xMDcuMzUyeiIgZmlsbD0iI2QwNWMwMCIvPjxwYXRoIGQ9Ik00NzIuMTEyIDExMy44NTV2MzQ3LjA2NkwzMjMuNjg5IDU2OC4yNzNWMjIxLjIwN2wxNDguNDIzLTEwNy4zNTJ6bS0xMC40OTkgMjAuNTUxTDMzNC4xODggMjI2LjU3djMyMS4xNTJsMTI3LjQyNS05Mi4xNjVWMTM0LjQwNXoiIGZpbGw9IiNmZmYiLz48cGF0aCBkPSJNNTIxLjEwNiAxMTMuODU1djM0Ny4wNjZMMzcyLjY4MyA1NjguMjczVjIyMS4yMDdsMTQ4LjQyMy0xMDcuMzUyeiIgZmlsbD0iI2QwNWMwMCIvPjxwYXRoIGQ9Ik01MjEuMTA2IDExMy44NTV2MzQ3LjA2NkwzNzIuNjgzIDU2OC4yNzNWMjIxLjIwN2wxNDguNDIzLTEwNy4zNTJ6bS0xMC40OTkgMjAuNTUxTDM4My4xODIgMjI2LjU3djMyMS4xNTJsMTI3LjQyNS05Mi4xNjVWMTM0LjQwNXoiIGZpbGw9IiNmZmYiLz48L2c+PHBhdGggZD0iTTY0Ny45NTIgMzMyLjkzOGMtOC43OTMgOC44MDMtMTguNjExIDE1LjMxMS0yOS40NDUgMTkuNTQ1LTEwLjgyNCA0LjIzNC0yMS45OTIgNi4zNDYtMzMuNTA3IDYuMzQ2LTExLjUwNCAwLTIyLjY3My0yLjExMi0zMy41MDctNi4zNDYtMTAuODI0LTQuMjM0LTIwLjY0Mi0xMC43NDItMjkuNDQ1LTE5LjU0NWwtMzguMDc2LTM4LjA3NmMtNS43NDctNS43NTctMTIuMDkzLTkuOTgxLTE5LjAzOC0xMi42OTJhNTguNzMgNTguNzMgMCAwIDAtMjEuNTc2LTQuMDYxIDU4LjgxIDU4LjgxIDAgMCAwLTIxLjU3NiA0LjA2MWMtNi45MzUgMi43MTEtMTMuMjgxIDYuOTM1LTE5LjAzOCAxMi42OTJsLTM0LjUyMiAzNC41MjItMjEuODMtMjEuODMgMzQuNTIyLTM0LjUyMmM4LjgwMy04LjgwMyAxOC42MjItMTUuMzExIDI5LjQ0NS0xOS41NDUgMTAuODM0LTQuMjM0IDIxLjgzLTYuMzQ2IDMyLjk5OS02LjM0NnMyMi4wODQgMi4xMTIgMzIuNzQ1IDYuMzQ2IDIwLjM5OCAxMC43NDIgMjkuMTkxIDE5LjU0NWwzOC4wNzYgMzguMDc2YzUuNzU3IDUuNzU3IDEyLjEwMyAxMC4wNzIgMTkuMDM4IDEyLjk0NiA2Ljk0NSAyLjg3MyAxNC4zMDYgNC4zMTUgMjIuMDg0IDQuMzE1IDcuNzg4IDAgMTUuMjMtMS40NDIgMjIuMzM4LTQuMzE1czEzLjU0NS03LjE4OSAxOS4yOTItMTIuOTQ2bDM0LjUyMi0zNC41MjIgMjEuODMgMjEuODMtMzQuNTIyIDM0LjUyMnptMCAxMDYuNjEyYy04Ljc5MyA4LjgwMy0xOC42MTEgMTUuMzExLTI5LjQ0NSAxOS41NDUtMTAuODI0IDQuMjM0LTIxLjk5MiA2LjM0Ni0zMy41MDcgNi4zNDYtMTEuNTA0IDAtMjIuNjczLTIuMTEyLTMzLjUwNy02LjM0Ni0xMC44MjQtNC4yMzQtMjAuNjQyLTEwLjc0Mi0yOS40NDUtMTkuNTQ1bC0zOC4wNzYtMzguMDc2Yy01Ljc0Ny01Ljc1Ny0xMi4wOTMtOS45ODEtMTkuMDM4LTEyLjY5MmE1OC43MyA1OC43MyAwIDAgMC0yMS41NzYtNC4wNjEgNTguODEgNTguODEgMCAwIDAtMjEuNTc2IDQuMDYxYy02LjkzNSAyLjcxMS0xMy4yODEgNi45MzUtMTkuMDM4IDEyLjY5MmwtMzQuNTIyIDM0LjUyMi0yMS44My0yMS4zMjIgMzQuNTIyLTM1LjAzYzguODAzLTguODAzIDE4LjYyMi0xNS4zMTEgMjkuNDQ1LTE5LjU0NSAxMC44MzQtNC4yMzQgMjEuODMtNi4zNDYgMzIuOTk5LTYuMzQ2czIyLjA4NCAyLjExMiAzMi43NDUgNi4zNDYgMjAuMzk4IDEwLjc0MiAyOS4xOTEgMTkuNTQ1bDM4LjA3NiAzOC4wNzZjNS43NTcgNS43NTcgMTIuMTg0IDEwLjA3MiAxOS4yOTIgMTIuOTQ2czE0LjU2IDQuMzE1IDIyLjMzOCA0LjMxNWM3Ljc4OCAwIDE1LjE0OS0xLjQ0MiAyMi4wODQtNC4zMTUgNi45NDUtMi44NzMgMTMuMjkxLTcuMTg5IDE5LjAzOC0xMi45NDZsMzQuNTIyLTM0LjUyMiAyMS44MyAyMS44My0zNC41MjIgMzQuNTIyem0tLjUwOCAxMDYuNjEyYy04Ljc5MyA4LjgwMy0xOC41MyAxNS4zMTEtMjkuMTkxIDE5LjU0NXMtMjEuNzM5IDYuMzQ2LTMzLjI1MyA2LjM0NmMtMTEuNTA0IDAtMjIuNjczLTIuMTEyLTMzLjUwNy02LjM0Ni0xMC44MjQtNC4yMzQtMjAuNjQyLTEwLjc0Mi0yOS40NDUtMTkuNTQ1bC0zOC41ODMtMzguMDc2Yy01Ljc0Ny01Ljc1Ny0xMi4wOTMtOS45ODEtMTkuMDM4LTEyLjY5MmE1OC43MyA1OC43MyAwIDAgMC0yMS41NzYtNC4wNjEgNTguODEgNTguODEgMCAwIDAtMjEuNTc2IDQuMDYxYy02LjkzNSAyLjcxMS0xMy4yODEgNi45MzUtMTkuMDM4IDEyLjY5MmwtMzQuNTIyIDM0LjUyMi0yMS4zMjItMjEuMzIyIDM0LjUyMi0zNS4wM2M4LjgwMy04LjgwMyAxOC41My0xNS4zMTEgMjkuMTkxLTE5LjU0NXMyMS41NzYtNi4zNDYgMzIuNzQ1LTYuMzQ2IDIyLjE3NSAyLjExMiAzMi45OTkgNi4zNDZjMTAuODM0IDQuMjM0IDIwLjY1MiAxMC43NDIgMjkuNDQ1IDE5LjU0NWwzOC4wNzYgMzguMDc2YzUuNzU3IDUuNzU3IDEyLjE4NCAxMC4wNzIgMTkuMjkyIDEyLjk0NnMxNC41NiA0LjMxNSAyMi4zMzggNC4zMTVjNy43ODggMCAxNS4xNDktMS40NDIgMjIuMDg0LTQuMzE1IDYuOTQ1LTIuODczIDEzLjI5MS03LjE4OSAxOS4wMzgtMTIuOTQ2bDM0LjUyMi0zNC41MjIgMjEuMzIyIDIxLjgzLTM0LjUyMiAzNC41MjJ6IiBmaWxsPSIjZmZmIiBmaWxsLXJ1bGU9Im5vbnplcm8iIHN0cm9rZT0iI2QwNWMwMCIgc3Ryb2tlLXdpZHRoPSI5LjAzNyIvPjwvc3ZnPg=="
TEMPERATURE_ALARM = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHZpZXdCb3g9IjAgMCA4MDAgODAwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHhtbG5zOnY9Imh0dHBzOi8vdmVjdGEuaW8vbmFubyI+PHBhdGggZD0iTS4wMDItLjAwMWg4MDAuMDAxdjgwMEguMDAyeiIgZmlsbD0iI2QwMDAwMCIvPjxnIHRyYW5zZm9ybT0ibWF0cml4KC45ODI5OTkgMCAwIC45ODI5OTkgODQuNDYzMyAxMjAuMzM3KSI+PHBhdGggZD0iTTM1Ni4zOTkgMzIuMzczYy0xOS41OTQtMzMuOTI0LTUxLjY0Ni0zMy45MjQtNzEuMjM4LS4wMDVsLTI3MC4yOSA0NjguMDJjLTE5LjU4NiAzMy45MjQtMy41NjMgNjEuNjgyIDM1LjYxNyA2MS42ODJoNTQxLjAwNmMzOS4xODIgMCA1NS4yMTMtMjcuNzU4IDM1LjYyMS02MS42ODJMMzU2LjM5OSAzMi4zNzMiIGZpbGw9IiNkMDAwMDAiIGZpbGwtcnVsZT0ibm9uemVybyIvPjxwYXRoIGQ9Ik0zNTYuMzk5IDMyLjM3M2MtMTkuNTk0LTMzLjkyNC01MS42NDYtMzMuOTI0LTcxLjIzOC0uMDA1bC0yNzAuMjkgNDY4LjAyYy0xOS41ODYgMzMuOTI0LTMuNTYzIDYxLjY4MiAzNS42MTcgNjEuNjgyaDU0MS4wMDZjMzkuMTgyIDAgNTUuMjEzLTI3Ljc1OCAzNS42MjEtNjEuNjgyTDM1Ni4zOTkgMzIuMzczeiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjIuNTEiLz48ZyBmaWxsLXJ1bGU9Im5vbnplcm8iIGZpbGw9IiNmZmYiPjxwYXRoIGQ9Ik04MC4yNiA1MDQuMDI1TDMyMS4yMTkgODYuNzUybDI0MC45NTggNDE3LjI3M0g4MC4yNm01MzMuMzA5IDcuMDQ4TDM0MC44MTEgMzguNzI5Yy0xMC43NzMtMTguNjU2LTI4LjQwMS0xOC42NTYtMzkuMTggMEwyOC44NzEgNTExLjA3M2MtMTAuNzcxIDE4LjY1Ni0xLjk1NCAzMy45MjQgMTkuNTk3IDMzLjkyNGg1NDUuNTExYzIxLjU0OSAwIDMwLjM2NS0xNS4yNjUgMTkuNTktMzMuOTI0eiIvPjxwYXRoIGQ9Ik0zMTQuNTg4IDE3Mi4yMjVjLTExLjMyMiAyLjQ3My0yMS4yMTIgMTEuNzEyLTI1LjI0NiAyMy42ODQtMS4wNDEgMy4xMjMtMS4wNDEgNy44MDgtMS4zMDEgOTkuOTQzbC0uMTMgOTYuNTU5LTMuNTE0IDMuNzc0Yy00LjAzNCA0LjQyNS04LjU4OSAxMi42MjMtMTAuMjgxIDE4Ljg2OS0xLjY5MiA1Ljg1Ni0yLjIxMiAxNS4zNTYtMS4xNzEgMjEuNDcyIDEuOTUyIDEyLjQ5MyA4Ljg0OSAyMy45NDUgMTguNzM5IDMxLjYyMyAxNS4zNTYgMTEuNzEyIDM1LjI2NiAxMy43OTQgNTIuNDQ0IDUuMzM1IDEwLjU0MS01LjIwNSAxNy42OTgtMTIuMzYzIDIyLjc3My0yMi41MTMgNC4wMzQtOC4wNjggNS4zMzUtMTQuMzE1IDQuOTQ1LTI0LjA3NS0uMjYtNi42MzctLjUyMS04LjcxOS0yLjA4Mi0xMy41MzQtMi4wODItNi4yNDYtNS43MjYtMTIuNzUzLTEwLjI4MS0xNy45NThsLTIuOTkzLTMuNTE0di05NC43MzhjMC0xMDQuNzU4LjEzLTk5LjAzMi0zLjkwNC0xMDcuMS02Ljg5Ny0xMy43OTQtMjIuNjQzLTIxLjA4Mi0zNy45OTktMTcuODI4em0xMy4xNDQgNi41MDdjMTEuMTkyIDIuMzQyIDE5Ljc4IDExLjMyMiAyMS40NzIgMjIuNTEzLjM5IDIuNjAzLjY1MSAzNi40MzguNjUxIDk5LjY4M3Y5NS43NzlsMi43MzMgMi42MDNjNC4yOTQgNC4wMzQgOC4xOTggMTAuNjcxIDEwLjE1IDE2LjUyNyAxLjU2MiA0Ljk0NSAxLjY5MiA2LjExNiAxLjY5MiAxMy43OTQgMCA3LjU0OC0uMjYgOC44NDktMS42OTIgMTMuMTQ0LTIuNDczIDcuNDE4LTUuNDY2IDEyLjEwMi0xMC44MDEgMTcuNDM4LTguMzI5IDguMzI5LTE2LjI2NyAxMS4zMjItMjkuODAxIDExLjMyMi02Ljg5NyAwLTguODQ5LS4yNi0xMi42MjMtMS40MzEtOS41LTIuOTkzLTE2LjM5Ny03LjgwOC0yMS42MDItMTUuMjI2LTEyLjEwMi0xNy4xNzgtMTAuODAxLTM5LjgyMSAyLjk5My01NC42NTZsNC4yOTQtNC41NTV2LTk3LjYwMWwxLjE3MS0xMDEuNTA1YzIuNzMzLTguOTc5IDEwLjY3MS0xNi4xMzcgMjAuMDQxLTE4LjA4OSA0Ljk0NS0uNjUxIDYuNTA3LS43ODEgMTEuMzIyLjI2em0tMTEuMTkyIDguMzI4Yy0yLjk5My43ODEtNy41NDggNC4xNjQtOS42MyA3LjAyNy00LjAzNCA1LjMzNS0zLjc3NC0xLjU2Mi0zLjc3NCAxMDcuMzYxdjk4LjUxMWwtNC44MTUgNC42ODVjLTMuNjQ0IDMuNjQ0LTUuMzM1IDUuODU2LTYuODk3IDkuMjQtNi43NjcgMTQuMTg1LTQuMjk0IDI4Ljg5IDYuNjM3IDM5Ljk1MSA1LjMzNSA1LjMzNSAxMS4wNjEgOC4zMjkgMTguNzM5IDkuNjMgMjAuOTUyIDMuNjQ0IDQwLjM0Mi0xMi44ODMgNDAuMzQyLTM0LjM1NSAwLTQuMTY0LTEuNjkyLTExLjU4Mi0zLjUxNC0xNS4wOTYtMS45NTItMy45MDQtNi4zNzctOS4zNy05LjM3LTExLjU4MmwtMi43MzMtMi4wODJ2LTIwLjE3MUgzMjYuNDN2LTQuMTY0aDE1LjA5NnYtMjcuNTg4SDMyNi40M3YtNC4xNjRoMTUuMDk2di0yNy41ODhIMzI2LjQzdi00LjE2NGgxNS4wOTZ2LTI3LjcxOUgzMjYuNDN2LTQuMTY0aDE1LjA5NnYtMjcuNzE5SDMyNi40M3YtNC4xNjRoMTUuMDk2di0yNy41ODhIMzI2LjQzdi00LjE2NGgxNS4wOTZsLS4yNi04LjU4OWMtLjEzLTcuODA4LS4zOS04LjcxOS0xLjgyMi0xMS41ODItMy41MTQtNi42MzctOS44OS0xMC41NDEtMTcuMDQ4LTEwLjQxMS0yLjA4MiAwLTQuODE1LjI2LTUuODU2LjY1MXoiLz48L2c+PC9nPjwvc3ZnPg=="
DOOR_OVERHEAT_ALARM = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHZpZXdCb3g9IjAgMCA4MDAgODAwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1saW5lY2FwPSJzcXVhcmUiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS1taXRlcmxpbWl0PSIxLjUiIHhtbG5zOnY9Imh0dHBzOi8vdmVjdGEuaW8vbmFubyI+PHBhdGggZD0iTS4wMDItLjAwMWg4MDAuMDAxdjgwMEguMDAyeiIgZmlsbD0iI2QwMDAwMCIvPjxnIHRyYW5zZm9ybT0ibWF0cml4KC45NDA2NCAwIDAgLjk0MDY0IC0xNzMuODczIDE0My42MTYpIj48cGF0aCBkPSJNNTQyLjA5NyAxMTQuMTgxdjM0Mi43OTdMMzM5LjU2MiA0NzMuNjdWMTMwLjg3M2wyMDIuNTM1LTE2LjY5MnoiIGZpbGw9IiNkMDAwMDAiLz48cGF0aCBkPSJNNTQyLjA5NyAxMTQuMTgxdjM0Mi43OTdMMzM5LjU2MiA0NzMuNjdWMTMwLjg3M2wyMDIuNTM1LTE2LjY5MnptLTE1Ljk0NyAxNy4zMTVsLTE3MC42NDEgMTQuMDYzdjMxMC43OTZsMTcwLjY0MS0xNC4wNjNWMTMxLjQ5NnoiIGZpbGw9IiNmZmYiLz48cGF0aCBkPSJNNTQyLjEwNCAxMTMuODU1djM0Ny4wNjZMMzkzLjY4MSA1NjguMjczVjIyMS4yMDdsMTQ4LjQyMy0xMDcuMzUyeiIgZmlsbD0iI2QwMDAwMCIvPjxwYXRoIGQ9Ik01NDIuMTA0IDExMy44NTV2MzQ3LjA2NkwzOTMuNjgxIDU2OC4yNzNWMjIxLjIwN2wxNDguNDIzLTEwNy4zNTJ6bS0xNS45NDcgMzEuMjE1bC0xMTYuNTI5IDg0LjI4NHYzMDcuNzA1bDExNi41MjktODQuMjg0VjE0NS4wN3oiIGZpbGw9IiNmZmYiLz48cGF0aCBkPSJNNDI3LjUyNSAzMDcuMTEzdjc4LjYzMSIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjE1Ljk1Ii8+PC9nPjxnIHRyYW5zZm9ybT0ibWF0cml4KC42MzIzOTMgMCAwIC42MzIzOTMgMjUyLjU5NyAxMTcuNDYxKSI+PHBhdGggZD0iTTM1Ni4zOTkgMzIuMzczYy0xOS41OTQtMzMuOTI0LTUxLjY0Ni0zMy45MjQtNzEuMjM4LS4wMDVsLTI3MC4yOSA0NjguMDJjLTE5LjU4NiAzMy45MjQtMy41NjMgNjEuNjgyIDM1LjYxNyA2MS42ODJoNTQxLjAwNmMzOS4xODIgMCA1NS4yMTMtMjcuNzU4IDM1LjYyMS02MS42ODJMMzU2LjM5OSAzMi4zNzMiIGZpbGw9IiNkMDAwMDAiIGZpbGwtcnVsZT0ibm9uemVybyIvPjxwYXRoIGQ9Ik0zNTYuMzk5IDMyLjM3M2MtMTkuNTk0LTMzLjkyNC01MS42NDYtMzMuOTI0LTcxLjIzOC0uMDA1bC0yNzAuMjkgNDY4LjAyYy0xOS41ODYgMzMuOTI0LTMuNTYzIDYxLjY4MiAzNS42MTcgNjEuNjgyaDU0MS4wMDZjMzkuMTgyIDAgNTUuMjEzLTI3Ljc1OCAzNS42MjEtNjEuNjgyTDM1Ni4zOTkgMzIuMzczeiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjIuNTEiIHN0cm9rZS1saW5lam9pbj0ibWl0ZXIiIHN0cm9rZS1taXRlcmxpbWl0PSI0Ii8+PGcgZmlsbC1ydWxlPSJub256ZXJvIiBmaWxsPSIjZmZmIj48cGF0aCBkPSJNODAuMjYgNTA0LjAyNUwzMjEuMjE5IDg2Ljc1MmwyNDAuOTU4IDQxNy4yNzNIODAuMjZtNTMzLjMwOSA3LjA0OEwzNDAuODExIDM4LjcyOWMtMTAuNzczLTE4LjY1Ni0yOC40MDEtMTguNjU2LTM5LjE4IDBMMjguODcxIDUxMS4wNzNjLTEwLjc3MSAxOC42NTYtMS45NTQgMzMuOTI0IDE5LjU5NyAzMy45MjRoNTQ1LjUxMWMyMS41NDkgMCAzMC4zNjUtMTUuMjY1IDE5LjU5LTMzLjkyNHoiLz48cGF0aCBkPSJNMzE0LjU4OCAxNzIuMjI1Yy0xMS4zMjIgMi40NzMtMjEuMjEyIDExLjcxMi0yNS4yNDYgMjMuNjg0LTEuMDQxIDMuMTIzLTEuMDQxIDcuODA4LTEuMzAxIDk5Ljk0M2wtLjEzIDk2LjU1OS0zLjUxNCAzLjc3NGMtNC4wMzQgNC40MjUtOC41ODkgMTIuNjIzLTEwLjI4MSAxOC44NjktMS42OTIgNS44NTYtMi4yMTIgMTUuMzU2LTEuMTcxIDIxLjQ3MiAxLjk1MiAxMi40OTMgOC44NDkgMjMuOTQ1IDE4LjczOSAzMS42MjMgMTUuMzU2IDExLjcxMiAzNS4yNjYgMTMuNzk0IDUyLjQ0NCA1LjMzNSAxMC41NDEtNS4yMDUgMTcuNjk4LTEyLjM2MyAyMi43NzMtMjIuNTEzIDQuMDM0LTguMDY4IDUuMzM1LTE0LjMxNSA0Ljk0NS0yNC4wNzUtLjI2LTYuNjM3LS41MjEtOC43MTktMi4wODItMTMuNTM0LTIuMDgyLTYuMjQ2LTUuNzI2LTEyLjc1My0xMC4yODEtMTcuOTU4bC0yLjk5My0zLjUxNHYtOTQuNzM4YzAtMTA0Ljc1OC4xMy05OS4wMzItMy45MDQtMTA3LjEtNi44OTctMTMuNzk0LTIyLjY0My0yMS4wODItMzcuOTk5LTE3LjgyOHptMTMuMTQ0IDYuNTA3YzExLjE5MiAyLjM0MiAxOS43OCAxMS4zMjIgMjEuNDcyIDIyLjUxMy4zOSAyLjYwMy42NTEgMzYuNDM4LjY1MSA5OS42ODN2OTUuNzc5bDIuNzMzIDIuNjAzYzQuMjk0IDQuMDM0IDguMTk4IDEwLjY3MSAxMC4xNSAxNi41MjcgMS41NjIgNC45NDUgMS42OTIgNi4xMTYgMS42OTIgMTMuNzk0IDAgNy41NDgtLjI2IDguODQ5LTEuNjkyIDEzLjE0NC0yLjQ3MyA3LjQxOC01LjQ2NiAxMi4xMDItMTAuODAxIDE3LjQzOC04LjMyOSA4LjMyOS0xNi4yNjcgMTEuMzIyLTI5LjgwMSAxMS4zMjItNi44OTcgMC04Ljg0OS0uMjYtMTIuNjIzLTEuNDMxLTkuNS0yLjk5My0xNi4zOTctNy44MDgtMjEuNjAyLTE1LjIyNi0xMi4xMDItMTcuMTc4LTEwLjgwMS0zOS44MjEgMi45OTMtNTQuNjU2bDQuMjk0LTQuNTU1di05Ny42MDFsMS4xNzEtMTAxLjUwNWMyLjczMy04Ljk3OSAxMC42NzEtMTYuMTM3IDIwLjA0MS0xOC4wODkgNC45NDUtLjY1MSA2LjUwNy0uNzgxIDExLjMyMi4yNnptLTExLjE5MiA4LjMyOGMtMi45OTMuNzgxLTcuNTQ4IDQuMTY0LTkuNjMgNy4wMjctNC4wMzQgNS4zMzUtMy43NzQtMS41NjItMy43NzQgMTA3LjM2MXY5OC41MTFsLTQuODE1IDQuNjg1Yy0zLjY0NCAzLjY0NC01LjMzNSA1Ljg1Ni02Ljg5NyA5LjI0LTYuNzY3IDE0LjE4NS00LjI5NCAyOC44OSA2LjYzNyAzOS45NTEgNS4zMzUgNS4zMzUgMTEuMDYxIDguMzI5IDE4LjczOSA5LjYzIDIwLjk1MiAzLjY0NCA0MC4zNDItMTIuODgzIDQwLjM0Mi0zNC4zNTUgMC00LjE2NC0xLjY5Mi0xMS41ODItMy41MTQtMTUuMDk2LTEuOTUyLTMuOTA0LTYuMzc3LTkuMzctOS4zNy0xMS41ODJsLTIuNzMzLTIuMDgydi0yMC4xNzFIMzI2LjQzdi00LjE2NGgxNS4wOTZ2LTI3LjU4OEgzMjYuNDN2LTQuMTY0aDE1LjA5NnYtMjcuNTg4SDMyNi40M3YtNC4xNjRoMTUuMDk2di0yNy43MTlIMzI2LjQzdi00LjE2NGgxNS4wOTZ2LTI3LjcxOUgzMjYuNDN2LTQuMTY0aDE1LjA5NnYtMjcuNTg4SDMyNi40M3YtNC4xNjRoMTUuMDk2bC0uMjYtOC41ODljLS4xMy03LjgwOC0uMzktOC43MTktMS44MjItMTEuNTgyLTMuNTE0LTYuNjM3LTkuODktMTAuNTQxLTE3LjA0OC0xMC40MTEtMi4wODIgMC00LjgxNS4yNi01Ljg1Ni42NTF6Ii8+PC9nPjwvZz48L3N2Zz4="
OBSTACLE_ALARM = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHZpZXdCb3g9IjAgMCA4MDAgODAwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1saW5lY2FwPSJzcXVhcmUiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS1taXRlcmxpbWl0PSIxLjUiIHhtbG5zOnY9Imh0dHBzOi8vdmVjdGEuaW8vbmFubyI+PHBhdGggZD0iTS4wMDItLjAwMWg4MDAuMDAxdjgwMEguMDAyeiIgZmlsbD0iI2QwMDAwMCIvPjxnIHRyYW5zZm9ybT0ibWF0cml4KC45NDA2NCAwIDAgLjk0MDY0IC0xNzMuODczIDE0My42MTYpIj48cGF0aCBkPSJNNTQyLjA5NyAxMTQuMTgxdjM0Mi43OTdMMzM5LjU2MiA0NzMuNjdWMTMwLjg3M2wyMDIuNTM1LTE2LjY5MnoiIGZpbGw9IiNkMDAwMDAiLz48cGF0aCBkPSJNNTQyLjA5NyAxMTQuMTgxdjM0Mi43OTdMMzM5LjU2MiA0NzMuNjdWMTMwLjg3M2wyMDIuNTM1LTE2LjY5MnptLTE1Ljk0NyAxNy4zMTVsLTE3MC42NDEgMTQuMDYzdjMxMC43OTZsMTcwLjY0MS0xNC4wNjNWMTMxLjQ5NnoiIGZpbGw9IiNmZmYiLz48cGF0aCBkPSJNNTQyLjEwNCAxMTMuODU1djM0Ny4wNjZMMzkzLjY4MSA1NjguMjczVjIyMS4yMDdsMTQ4LjQyMy0xMDcuMzUyeiIgZmlsbD0iI2QwMDAwMCIvPjxwYXRoIGQ9Ik01NDIuMTA0IDExMy44NTV2MzQ3LjA2NkwzOTMuNjgxIDU2OC4yNzNWMjIxLjIwN2wxNDguNDIzLTEwNy4zNTJ6bS0xNS45NDcgMzEuMjE1bC0xMTYuNTI5IDg0LjI4NHYzMDcuNzA1bDExNi41MjktODQuMjg0VjE0NS4wN3oiIGZpbGw9IiNmZmYiLz48cGF0aCBkPSJNNDI3LjUyNSAzMDcuMTEzdjc4LjYzMSIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjE1Ljk1Ii8+PC9nPjxwYXRoIGQ9Ik00NzcuOTgxIDEzNy45MzNjLTEyLjM5MS0yMS40NTMtMzIuNjYxLTIxLjQ1My00NS4wNS0uMDAzbC0xNzAuOTMgMjk1Ljk3M2MtMTIuMzg2IDIxLjQ1My0yLjI1MyAzOS4wMDcgMjIuNTI0IDM5LjAwN2gzNDIuMTI4YzI0Ljc3OCAwIDM0LjkxNi0xNy41NTQgMjIuNTI2LTM5LjAwN0w0NzcuOTgxIDEzNy45MzMiIGZpbGw9IiNkMDAwMDAiIGZpbGwtcnVsZT0ibm9uemVybyIvPjxwYXRoIGQ9Ik00NzcuOTgxIDEzNy45MzNjLTEyLjM5MS0yMS40NTMtMzIuNjYxLTIxLjQ1My00NS4wNS0uMDAzbC0xNzAuOTMgMjk1Ljk3M2MtMTIuMzg2IDIxLjQ1My0yLjI1MyAzOS4wMDcgMjIuNTI0IDM5LjAwN2gzNDIuMTI4YzI0Ljc3OCAwIDM0LjkxNi0xNy41NTQgMjIuNTI2LTM5LjAwN0w0NzcuOTgxIDEzNy45MzN6IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmYiIHN0cm9rZS1saW5lam9pbj0ibWl0ZXIiIHN0cm9rZS1taXRlcmxpbWl0PSI0IiBzdHJva2Utd2lkdGg9IjEuNTg3Ii8+PGcgZmlsbC1ydWxlPSJub256ZXJvIiBmaWxsPSIjZmZmIj48cGF0aCBkPSJNMzAzLjM1MyA0MzYuMjAzbDE1Mi4zODEtMjYzLjg4MSAxNTIuMzggMjYzLjg4MUgzMDMuMzUzbTMzNy4yNjEgNC40NTdsLTE3Mi40OS0yOTguNzA3Yy02LjgxMy0xMS43OTgtMTcuOTYxLTExLjc5OC0yNC43NzcgMEwyNzAuODU1IDQ0MC42NmMtNi44MTIgMTEuNzk4LTEuMjM2IDIxLjQ1MyAxMi4zOTMgMjEuNDUzaDM0NC45NzdjMTMuNjI3IDAgMTkuMjAzLTkuNjUzIDEyLjM4OS0yMS40NTN6Ii8+PHBhdGggZD0iTTQ1NS4yOTQgNDE2LjU1M2EyMC43OSAyMC43OSAwIDAgMCAyMC43ODktMjAuNzgxIDIwLjc5IDIwLjc5IDAgMCAwLTIwLjc4OS0yMC43ODJjLTExLjQ4MiAwLTIwLjc4OSA5LjMwMy0yMC43ODkgMjAuNzgyczkuMzA3IDIwLjc4MSAyMC43ODkgMjAuNzgxbTIwLjY2LTE2My42ODNjLjE1OC0xLjAzOC4xMjctLjIwOC4xMjctMS4yOTEgMC0xMS40NzktOS4zMDktMjAuNzg1LTIwLjc4OS0yMC43ODVzLTIwLjc4OSA5LjMwNi0yMC43ODkgMjAuNzg1YTIxLjg1IDIxLjg1IDAgMCAwIC4wNDQgMS4yOTFoLS4wMTNsNy44NDQgOTEuMDY1aC4wMThjLjMxNyA2Ljg1OCA1Ljk1NyAxMi4zMjMgMTIuODk0IDEyLjMyMyA3LjEzNyAwIDEyLjgxMS01LjM2OSAxMi45MTMtMTIuMzIzbC4wMDgtLjY2NSA3Ljc0My05MC40Ii8+PC9nPjwvc3ZnPg=="
POWER_FAILURE_ALARM = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHZpZXdCb3g9IjAgMCA4MDAgODAwIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHhtbG5zOnY9Imh0dHBzOi8vdmVjdGEuaW8vbmFubyI+PHBhdGggZD0iTS4wMDItLjAwMWg4MDAuMDAxdjgwMEguMDAyeiIgZmlsbD0iI2QwMDAwMCIvPjxwYXRoIGQ9Ik00MDAgMTU0bDI4NCA0OTJIMTE2bDI4NC00OTJ6IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmYiIHN0cm9rZS13aWR0aD0iMzIiLz48cGF0aCBkPSJNMzc4IDMwMmwtNTAgMTc3IDc3LTQxLTE5IDExOS0xNi0yMiAxNSA3MiA0MS02MS0yMyAxNCA0NS0xNjQtODAgNDMgNTktMTM3IiBmaWxsPSIjZmZmIiBmaWxsLXJ1bGU9Im5vbnplcm8iLz48L3N2Zz4="
