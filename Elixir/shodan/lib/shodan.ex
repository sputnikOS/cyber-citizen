defmodule ShodanClient do
  use HTTPoison.Base

  @base_url "https://api.shodan.io"

  def process_request(method, url, body, headers, options) do
    url = "#{@base_url}#{url}"
    headers = [{"Accept", "application/json"} | headers]
    HTTPoison.request(method, url, body, headers, options)
  end

  def search(api_key, query) do
    path = "/shodan/host/search"
    params = %{"query" => query, "key" => api_key}
    case get(path, params) do
      {:ok, %HTTPoison.Response{status_code: 200, body: body}} ->
        case Jason.decode(body) do
          {:ok, decoded} -> {:ok, decoded}
          {:error, reason} -> {:error, "Failed to decode JSON: #{reason}"}
        end
      {:ok, %HTTPoison.Response{status_code: status_code}} ->
        {:error, "Request failed with status: #{status_code}"}
      {:error, reason} ->
        {:error, "Failed to make request: #{inspect(reason)}"}
    end
  end

  def get(path, params \\ %{}, headers \\ []) do
    HTTPoison.get(@base_url <> path, params, headers)
  end
end
