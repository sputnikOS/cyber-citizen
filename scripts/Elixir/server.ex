web_server.exs/e

defmodule WebServer do
  def start do
    Application.ensure_all_started(:my_web_app)
    IO.puts("Web server started at http://localhost:4000")
    IO.puts("Press Ctrl+C to stop the server")
    IO.gets()
  end
end

WebServer.start()
