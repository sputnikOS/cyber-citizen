defmodule ShodanTest do
  use ExUnit.Case
  doctest Shodan

  test "greets the world" do
    assert Shodan.hello() == :world
  end
end
