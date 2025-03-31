"""Tests for pattern matching against downloaded GitHub release JSONs."""

import json
from pathlib import Path

import pytest

from dotbins.config import build_tool_config


@pytest.mark.parametrize(
    ("program", "platform", "arch", "expected_asset"),
    [
        ("bandwhich", "linux", "amd64", "bandwhich-v0.23.1-x86_64-unknown-linux-gnu.tar.gz"),
        ("bandwhich", "linux", "arm64", "bandwhich-v0.23.1-aarch64-unknown-linux-gnu.tar.gz"),
        ("bandwhich", "macos", "arm64", "bandwhich-v0.23.1-aarch64-apple-darwin.tar.gz"),
        ("bat", "linux", "amd64", "bat-v0.25.0-x86_64-unknown-linux-gnu.tar.gz"),
        ("bat", "linux", "arm64", "bat-v0.25.0-aarch64-unknown-linux-gnu.tar.gz"),
        ("bat", "macos", "arm64", "bat-v0.25.0-aarch64-apple-darwin.tar.gz"),
        ("btm", "linux", "amd64", "bottom_x86_64-unknown-linux-gnu-2-17.tar.gz"),
        ("btm", "linux", "arm64", "bottom_aarch64-unknown-linux-gnu.tar.gz"),
        ("btm", "macos", "arm64", "bottom_aarch64-apple-darwin.tar.gz"),
        ("btop", "linux", "amd64", "btop-x86_64-linux-musl.tbz"),
        ("btop", "linux", "arm64", "btop-aarch64-linux-musl.tbz"),
        ("caddy", "linux", "amd64", "caddy_2.9.1_linux_amd64.tar.gz"),
        ("caddy", "linux", "arm64", "caddy_2.9.1_linux_arm64.tar.gz"),
        ("caddy", "macos", "arm64", "caddy_2.9.1_mac_arm64.tar.gz"),
        ("choose", "linux", "amd64", "choose-x86_64-unknown-linux-gnu"),
        ("choose", "linux", "arm64", "choose-aarch64-unknown-linux-gnu"),
        ("choose", "macos", "arm64", "choose-aarch64-apple-darwin"),
        ("croc", "linux", "amd64", None),  # Expect no match due to ambiguous detection
        ("croc", "linux", "arm64", "croc_v10.2.2_Linux-ARM64.tar.gz"),
        ("croc", "macos", "arm64", "croc_v10.2.2_macOS-ARM64.tar.gz"),
        ("ctop", "linux", "amd64", "ctop-0.7.7-linux-amd64"),
        ("ctop", "linux", "arm64", "ctop-0.7.7-linux-arm64"),
        ("ctop", "macos", "arm64", "ctop-0.7.7-darwin-amd64"),
        ("curlie", "linux", "amd64", "curlie_1.8.2_linux_amd64.tar.gz"),
        ("curlie", "linux", "arm64", "curlie_1.8.2_linux_arm64.tar.gz"),
        ("curlie", "macos", "arm64", "curlie_1.8.2_darwin_arm64.tar.gz"),
        ("delta", "linux", "amd64", "delta-0.18.2-x86_64-unknown-linux-gnu.tar.gz"),
        ("delta", "linux", "arm64", "delta-0.18.2-aarch64-unknown-linux-gnu.tar.gz"),
        ("delta", "macos", "arm64", "delta-0.18.2-aarch64-apple-darwin.tar.gz"),
        ("difft", "linux", "amd64", "difft-x86_64-unknown-linux-gnu.tar.gz"),
        ("difft", "linux", "arm64", "difft-aarch64-unknown-linux-gnu.tar.gz"),
        ("difft", "macos", "arm64", "difft-aarch64-apple-darwin.tar.gz"),
        ("direnv", "linux", "amd64", "direnv.linux-amd64"),
        ("direnv", "linux", "arm64", "direnv.linux-arm64"),
        ("direnv", "macos", "arm64", "direnv.darwin-arm64"),
        ("dog", "linux", "amd64", "dog-v0.1.0-x86_64-unknown-linux-gnu.zip"),
        ("duf", "linux", "amd64", "duf_0.8.1_linux_x86_64.tar.gz"),
        ("duf", "linux", "arm64", "duf_0.8.1_linux_arm64.tar.gz"),
        ("duf", "macos", "arm64", "duf_0.8.1_Darwin_arm64.tar.gz"),
        ("dust", "linux", "amd64", "dust-v1.1.2-x86_64-unknown-linux-gnu.tar.gz"),
        ("dust", "linux", "arm64", "dust-v1.1.2-aarch64-unknown-linux-gnu.tar.gz"),
        ("eget", "linux", "amd64", "eget-1.3.4-linux_amd64.tar.gz"),
        ("eget", "linux", "arm64", "eget-1.3.4-linux_arm64.tar.gz"),
        ("eget", "macos", "arm64", "eget-1.3.4-darwin_arm64.tar.gz"),
        ("fd", "linux", "amd64", "fd-v10.2.0-x86_64-unknown-linux-gnu.tar.gz"),
        ("fd", "linux", "arm64", "fd-v10.2.0-aarch64-unknown-linux-gnu.tar.gz"),
        ("fd", "macos", "arm64", "fd-v10.2.0-aarch64-apple-darwin.tar.gz"),
        ("fzf", "linux", "amd64", "fzf-0.61.0-linux_amd64.tar.gz"),
        ("fzf", "linux", "arm64", "fzf-0.61.0-linux_arm64.tar.gz"),
        ("fzf", "macos", "arm64", "fzf-0.61.0-darwin_arm64.tar.gz"),
        ("git-lfs", "linux", "amd64", "git-lfs-linux-amd64-v3.6.1.tar.gz"),
        ("git-lfs", "linux", "arm64", "git-lfs-linux-arm64-v3.6.1.tar.gz"),
        ("git-lfs", "macos", "arm64", "git-lfs-darwin-arm64-v3.6.1.zip"),
        ("glow", "linux", "amd64", "glow_2.1.0_Linux_x86_64.tar.gz"),
        ("glow", "linux", "arm64", "glow_2.1.0_Linux_arm64.tar.gz"),
        ("glow", "macos", "arm64", "glow_2.1.0_Darwin_arm64.tar.gz"),
        ("gping", "linux", "amd64", "gping-Linux-gnu-x86_64.tar.gz"),
        ("gping", "linux", "arm64", "gping-Linux-gnu-arm64.tar.gz"),
        ("gping", "macos", "arm64", "gping-macOS-arm64.tar.gz"),
        ("grex", "linux", "amd64", "grex-v1.4.5-x86_64-unknown-linux-musl.tar.gz"),
        ("grex", "linux", "arm64", "grex-v1.4.5-aarch64-unknown-linux-musl.tar.gz"),
        ("grex", "macos", "arm64", "grex-v1.4.5-aarch64-apple-darwin.tar.gz"),
        ("gron", "linux", "amd64", "gron-linux-amd64-0.7.1.tgz"),
        ("gron", "linux", "arm64", "gron-linux-arm64-0.7.1.tgz"),
        ("gron", "macos", "arm64", "gron-darwin-arm64-0.7.1.tgz"),
        ("hexyl", "linux", "amd64", "hexyl-v0.16.0-x86_64-unknown-linux-gnu.tar.gz"),
        ("hexyl", "linux", "arm64", "hexyl-v0.16.0-aarch64-unknown-linux-gnu.tar.gz"),
        ("hexyl", "macos", "arm64", "hexyl-v0.16.0-aarch64-apple-darwin.tar.gz"),
        ("hx", "linux", "amd64", "helix-25.01.1-x86_64.AppImage"),
        ("hx", "linux", "arm64", "helix-25.01.1-aarch64-linux.tar.xz"),
        ("hx", "macos", "arm64", "helix-25.01.1-aarch64-macos.tar.xz"),
        ("hyperfine", "linux", "amd64", "hyperfine-v1.19.0-x86_64-unknown-linux-gnu.tar.gz"),
        ("hyperfine", "linux", "arm64", "hyperfine-v1.19.0-aarch64-unknown-linux-gnu.tar.gz"),
        ("hyperfine", "macos", "arm64", "hyperfine-v1.19.0-aarch64-apple-darwin.tar.gz"),
        ("jc", "linux", "amd64", "jc-1.25.4-linux-x86_64.tar.gz"),
        ("jc", "linux", "arm64", "jc-1.25.4-linux-aarch64.tar.gz"),
        ("jc", "macos", "arm64", "jc-1.25.4-darwin-aarch64.tar.gz"),
        ("jless", "linux", "amd64", "jless-v0.9.0-x86_64-unknown-linux-gnu.zip"),
        ("jless", "macos", "arm64", "jless-v0.9.0-aarch64-apple-darwin.zip"),
        ("jq", "linux", "amd64", "jq-linux-amd64"),
        ("jq", "linux", "arm64", "jq-linux-arm64"),
        ("jq", "macos", "arm64", "jq-macos-arm64"),
        ("just", "linux", "amd64", "just-1.40.0-x86_64-unknown-linux-musl.tar.gz"),
        ("just", "linux", "arm64", "just-1.40.0-aarch64-unknown-linux-musl.tar.gz"),
        ("just", "macos", "arm64", "just-1.40.0-aarch64-apple-darwin.tar.gz"),
        ("k9s", "linux", "amd64", "k9s_Linux_amd64.tar.gz"),
        ("k9s", "linux", "arm64", "k9s_Linux_arm64.tar.gz"),
        ("k9s", "macos", "arm64", "k9s_Darwin_arm64.tar.gz"),
        ("lazygit", "linux", "amd64", "lazygit_0.48.0_Linux_x86_64.tar.gz"),
        ("lazygit", "linux", "arm64", "lazygit_0.48.0_Linux_arm64.tar.gz"),
        ("lazygit", "macos", "arm64", "lazygit_0.48.0_Darwin_arm64.tar.gz"),
        ("lnav", "linux", "amd64", "lnav-0.12.4-linux-musl-x86_64.zip"),
        ("lnav", "linux", "arm64", "lnav-0.12.4-linux-musl-arm64.zip"),
        ("lnav", "macos", "arm64", "lnav-0.12.4-aarch64-macos.zip"),
        ("lsd", "linux", "amd64", "lsd-v1.1.5-x86_64-unknown-linux-gnu.tar.gz"),
        ("lsd", "linux", "arm64", "lsd-v1.1.5-aarch64-unknown-linux-gnu.tar.gz"),
        ("lsd", "macos", "arm64", "lsd-v1.1.5-aarch64-apple-darwin.tar.gz"),
        ("mcfly", "linux", "amd64", "mcfly-v0.9.3-x86_64-unknown-linux-musl.tar.gz"),
        ("mcfly", "linux", "arm64", "mcfly-v0.9.3-aarch64-unknown-linux-gnu.tar.gz"),
        ("micro", "linux", "amd64", "micro-2.0.14-linux64-static.tar.gz"),
        ("micro", "linux", "arm64", "micro-2.0.14-linux-arm64.tar.gz"),
        ("micro", "macos", "arm64", "micro-2.0.14-macos-arm64.tar.gz"),
        ("navi", "linux", "amd64", "navi-v2.24.0-x86_64-unknown-linux-musl.tar.gz"),
        ("navi", "linux", "arm64", "navi-v2.24.0-aarch64-unknown-linux-gnu.tar.gz"),
        ("neovim", "linux", "amd64", "nvim-linux-x86_64.appimage"),
        ("neovim", "linux", "arm64", "nvim-linux-arm64.appimage"),
        ("neovim", "macos", "amd64", "nvim-macos-x86_64.tar.gz"),
        ("neovim", "macos", "arm64", "nvim-macos-arm64.tar.gz"),
        ("nu", "linux", "amd64", "nu-0.103.0-x86_64-unknown-linux-gnu.tar.gz"),
        ("nu", "linux", "arm64", "nu-0.103.0-aarch64-unknown-linux-gnu.tar.gz"),
        ("nu", "macos", "arm64", "nu-0.103.0-aarch64-apple-darwin.tar.gz"),
        ("pastel", "linux", "amd64", "pastel-v0.10.0-x86_64-unknown-linux-gnu.tar.gz"),
        ("pastel", "linux", "arm64", "pastel-v0.10.0-aarch64-unknown-linux-gnu.tar.gz"),
        ("procs", "linux", "amd64", "procs-v0.14.10-x86_64-linux.zip"),
        ("procs", "linux", "arm64", "procs-v0.14.10-aarch64-linux.zip"),
        ("procs", "macos", "arm64", "procs-v0.14.10-aarch64-mac.zip"),
        ("rg", "linux", "amd64", "ripgrep-14.1.1-x86_64-unknown-linux-musl.tar.gz"),
        ("rg", "linux", "arm64", "ripgrep-14.1.1-aarch64-unknown-linux-gnu.tar.gz"),
        ("rg", "macos", "arm64", "ripgrep-14.1.1-aarch64-apple-darwin.tar.gz"),
        ("rip", "linux", "amd64", "rip-Linux-x86_64-musl.tar.gz"),
        ("rip", "linux", "arm64", "rip-Linux-aarch64-musl.tar.gz"),
        ("rip", "macos", "arm64", "rip-macOS-Darwin-aarch64.tar.gz"),
        ("sd", "linux", "amd64", "sd-v1.0.0-x86_64-unknown-linux-gnu.tar.gz"),
        ("sd", "linux", "arm64", "sd-v1.0.0-aarch64-unknown-linux-musl.tar.gz"),
        ("sd", "macos", "arm64", "sd-v1.0.0-aarch64-apple-darwin.tar.gz"),
        ("sk", "linux", "amd64", "skim-x86_64-unknown-linux-musl.tgz"),
        ("sk", "linux", "arm64", "skim-aarch64-unknown-linux-musl.tgz"),
        ("sk", "macos", "arm64", "skim-aarch64-apple-darwin.tgz"),
        ("starship", "linux", "amd64", "starship-x86_64-unknown-linux-gnu.tar.gz"),
        ("starship", "linux", "arm64", "starship-aarch64-unknown-linux-musl.tar.gz"),
        ("starship", "macos", "arm64", "starship-aarch64-apple-darwin.tar.gz"),
        ("tldr", "linux", "amd64", "tealdeer-linux-x86_64-musl"),
        ("tldr", "linux", "arm64", "tealdeer-linux-aarch64-musl"),
        ("tldr", "macos", "arm64", "tealdeer-macos-aarch64"),
        ("topgrade", "linux", "amd64", "topgrade-v16.0.2-x86_64-unknown-linux-gnu.tar.gz"),
        ("topgrade", "linux", "arm64", "topgrade-v16.0.2-aarch64-unknown-linux-gnu.tar.gz"),
        ("topgrade", "macos", "arm64", "topgrade-v16.0.2-aarch64-apple-darwin.tar.gz"),
        ("tre", "linux", "amd64", "tre-v0.4.0-x86_64-unknown-linux-musl.tar.gz"),
        ("tre", "macos", "arm64", "tre-v0.4.0-aarch64-apple-darwin.tar.gz"),
        ("xh", "linux", "amd64", "xh-v0.24.0-x86_64-unknown-linux-musl.tar.gz"),
        ("xh", "linux", "arm64", "xh-v0.24.0-aarch64-unknown-linux-musl.tar.gz"),
        ("xh", "macos", "arm64", "xh-v0.24.0-aarch64-apple-darwin.tar.gz"),
        ("xplr", "linux", "arm64", "xplr-linux-aarch64.tar.gz"),
        ("xplr", "macos", "arm64", "xplr-macos-aarch64.tar.gz"),
        ("yazi", "linux", "amd64", "yazi-x86_64-unknown-linux-gnu.zip"),
        ("yazi", "linux", "arm64", "yazi-aarch64-unknown-linux-gnu.zip"),
        ("yazi", "macos", "arm64", "yazi-aarch64-apple-darwin.zip"),
        ("yq", "linux", "amd64", "yq_linux_amd64"),
        ("yq", "linux", "arm64", "yq_linux_arm64"),
        ("yq", "macos", "arm64", "yq_darwin_arm64"),
        ("zellij", "linux", "amd64", "zellij-x86_64-unknown-linux-musl.tar.gz"),
        ("zellij", "linux", "arm64", "zellij-aarch64-unknown-linux-musl.tar.gz"),
        ("zellij", "macos", "arm64", "zellij-aarch64-apple-darwin.tar.gz"),
        ("zoxide", "linux", "amd64", "zoxide-0.9.7-x86_64-unknown-linux-musl.tar.gz"),
        ("zoxide", "linux", "arm64", "zoxide-0.9.7-aarch64-unknown-linux-musl.tar.gz"),
        ("zoxide", "macos", "arm64", "zoxide-0.9.7-aarch64-apple-darwin.tar.gz"),
    ],
)
def test_autodetect_asset(program: str, platform: str, arch: str, expected_asset: str) -> None:
    """Test that the correct asset is selected from the release JSON.

    This test:
    1. Loads a real release JSON from the tests/release_jsons directory
    2. Creates a ToolConfig for the tool
    3. Verifies that we can find a matching asset for each platform/arch combination
    """
    # Load the release JSON
    json_file = Path(__file__).parent / "release_jsons" / f"{program}.json"
    with open(json_file) as f:
        release_data = json.load(f)

    # Create tool config
    tool_config = build_tool_config(
        tool_name=program,
        raw_data={"repo": f"example/{program}"},
        platforms={platform: [arch]},
    )

    # Set the latest release data directly
    tool_config._latest_release = release_data

    # Test asset selection
    bin_spec = tool_config.bin_spec(arch, platform)
    matching_asset = bin_spec.matching_asset()

    if expected_asset is None:
        # For cases where we expect ambiguous detection, assert that no asset is found
        assert matching_asset is None, f"Expected no match due to ambiguity, but found: {matching_asset}"
    else:
        # For normal cases, assert that the correct asset is found
        assert matching_asset is not None
        assert matching_asset["name"] == expected_asset
