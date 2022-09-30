using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class AudioVisualizer : MonoBehaviour {
		
	public Transform[] audioSpectrumObjects;
	[Range(1, 100)] public float heightMultiplier; //Here is the public range for Cylinder 
	[Range(64, 8192)] public int numberOfSamples = 1024; //step by 2
	public FFTWindow fftWindow;
	public float lerpTime = 1;
	public Slider sensitivitySlider;

	void Start(){

		heightMultiplier = PlayerPrefsManager.GetSensitivity ();

		sensitivitySlider.onValueChanged.AddListener(delegate {
			SensitivityValueChangedHandler(sensitivitySlider);
		});
	}

	void Update() {

		// initialize our float array
		float[] spectrum = new float[numberOfSamples];

		GetComponent<AudioSource>().GetSpectrumData(spectrum, 0, fftWindow);

		for(int i = 0; i < audioSpectrumObjects.Length; i++)
		{

			
			float intensity = spectrum[i] * heightMultiplier;

			// calculate object's scale
			float lerpY = Mathf.Lerp(audioSpectrumObjects[i].localScale.y,intensity,lerpTime);
			Vector3 newScale = new Vector3( audioSpectrumObjects[i].localScale.x, lerpY, audioSpectrumObjects[i].localScale.z);

			audioSpectrumObjects[i].localScale = newScale;

		}
	}

	public void SensitivityValueChangedHandler(Slider sensitivitySlider){
		heightMultiplier = 400f;
	}

}
