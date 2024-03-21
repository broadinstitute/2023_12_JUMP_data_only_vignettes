{ pkgs ? import <nixpkgs> {} }:

let
  inherit (pkgs) fetchFromGitHub callPackage;

  poetry2nix-src = fetchFromGitHub {
      owner = "nix-community";
      repo = "poetr y2nix";
      rev = "7df29134065172f24385177ea69e755cb90f196c";
      sha256 = "0zz3qzp2b5i9gw4yfxfrq07iadcdadackph12h02w19bb3535rm6";
  };

  poetry2nix = callPackage poetry2nix-src { };

in
  poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    preferWheels = true; # TODO use overrides to fix this
    # It has to do with the maturin rust dependencies
}
