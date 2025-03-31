class Trmd < Formula
  include Language::Python::Virtualenv

  desc "Translate Markdown using OpenAI"
  homepage "https://github.com/rioriost/homebrew-trmd/"
  url "https://files.pythonhosted.org/packages/78/0d/2fd64982a3721d4c8ef90fea3b0c286ce1018582d7df95f4336241004b4e/trmd-0.1.0.tar.gz"
  sha256 "d5102f10892dbab8b965b8946e63050486e7e273cc78791df266960431d4c914"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
    system libexec/"bin/python", "-m", "pip", "install", "openai"
  end

  test do
    system "#{bin}/trmd", "--help"
  end
end
