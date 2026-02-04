const hre = require("hardhat");

async function main() {
  console.log("🚀 Deploying AgentMarketplace...\n");

  // Sepolia USDC address (Circle's official testnet USDC)
  const SEPOLIA_USDC = "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238";

  // Get deployer
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with account:", deployer.address);
  console.log("Account balance:", (await hre.ethers.provider.getBalance(deployer.address)).toString(), "\n");

  // Deploy AgentMarketplace
  const AgentMarketplace = await hre.ethers.getContractFactory("AgentMarketplace");
  const marketplace = await AgentMarketplace.deploy(SEPOLIA_USDC);

  await marketplace.waitForDeployment();

  const address = await marketplace.getAddress();

  console.log("✅ AgentMarketplace deployed to:", address);
  console.log("📝 USDC Token:", SEPOLIA_USDC);
  console.log("👤 Owner:", deployer.address);
  console.log("\n🔗 Sepolia Etherscan:", `https://sepolia.etherscan.io/address/${address}`);

  // Save deployment info
  const fs = require('fs');
  const deploymentInfo = {
    network: "sepolia",
    contractAddress: address,
    usdcAddress: SEPOLIA_USDC,
    owner: deployer.address,
    deployedAt: new Date().toISOString(),
    blockNumber: await hre.ethers.provider.getBlockNumber()
  };

  fs.writeFileSync(
    '../DEPLOYMENT.json',
    JSON.stringify(deploymentInfo, null, 2)
  );

  console.log("\n💾 Deployment info saved to DEPLOYMENT.json");

  // Wait for block confirmations before verifying
  console.log("\n⏳ Waiting for block confirmations...");
  await marketplace.deploymentTransaction().wait(6);

  // Verify on Etherscan
  console.log("\n🔍 Verifying contract on Etherscan...");
  try {
    await hre.run("verify:verify", {
      address: address,
      constructorArguments: [SEPOLIA_USDC],
    });
    console.log("✅ Contract verified!");
  } catch (error) {
    console.log("❌ Verification failed:", error.message);
    console.log("You can verify manually later with:");
    console.log(`npx hardhat verify --network sepolia ${address} ${SEPOLIA_USDC}`);
  }

  console.log("\n🎉 Deployment complete!");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
